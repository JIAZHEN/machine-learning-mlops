"""
Data drift monitoring module using Evidently AI.

Monitors data quality and drift for production ML models:
- Distribution drift detection
- Data quality checks
- Target drift monitoring
- Feature drift tracking
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, Optional
import logging

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, TargetDriftPreset
from evidently.test_suite import TestSuite
from evidently.tests import (
    TestNumberOfColumns,
    TestNumberOfRows,
    TestColumnsType,
    TestNumberOfDriftedColumns,
    TestShareOfDriftedColumns,
)

logger = logging.getLogger(__name__)


class DriftMonitor:
    """Monitor data drift for churn prediction model."""
    
    def __init__(self, reference_data_path: str, output_dir: str = "reports/drift"):
        """
        Initialize drift monitor.
        
        Args:
            reference_data_path: Path to reference dataset (training data)
            output_dir: Directory to save drift reports
        """
        self.reference_data = pd.read_csv(reference_data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define column mapping for Evidently
        self.column_mapping = ColumnMapping(
            target='Churn' if 'Churn' in self.reference_data.columns else None,
            numerical_features=self._get_numerical_features(),
            categorical_features=self._get_categorical_features()
        )
        
        logger.info(f"DriftMonitor initialized with reference data: {len(self.reference_data)} rows")
    
    def _get_numerical_features(self) -> list:
        """Get numerical feature names."""
        numeric_cols = self.reference_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        # Exclude target and ID columns
        exclude = ['Churn', 'customerID']
        return [col for col in numeric_cols if col not in exclude]
    
    def _get_categorical_features(self) -> list:
        """Get categorical feature names."""
        cat_cols = self.reference_data.select_dtypes(include=['object']).columns.tolist()
        # Exclude target and ID columns
        exclude = ['Churn', 'customerID']
        return [col for col in cat_cols if col not in exclude]
    
    def generate_drift_report(
        self, 
        current_data: pd.DataFrame,
        save_html: bool = True,
        save_json: bool = True
    ) -> Dict:
        """
        Generate comprehensive drift report.
        
        Args:
            current_data: Current production data to compare
            save_html: Save HTML report
            save_json: Save JSON report
            
        Returns:
            Dictionary with drift metrics
        """
        logger.info("Generating drift report...")
        
        # Create report with multiple presets
        report = Report(metrics=[
            DataDriftPreset(),
            DataQualityPreset(),
        ])
        
        # Run report
        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )
        
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save HTML report
        if save_html:
            html_path = self.output_dir / f"drift_report_{timestamp}.html"
            report.save_html(str(html_path))
            logger.info(f"HTML report saved: {html_path}")
        
        # Get metrics as JSON
        report_json = report.as_dict()
        
        # Save JSON report
        if save_json:
            json_path = self.output_dir / f"drift_metrics_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(report_json, f, indent=2)
            logger.info(f"JSON metrics saved: {json_path}")
        
        # Extract key metrics
        drift_summary = self._extract_drift_summary(report_json)
        
        return drift_summary
    
    def run_drift_tests(self, current_data: pd.DataFrame) -> Dict:
        """
        Run automated drift tests.
        
        Args:
            current_data: Current production data
            
        Returns:
            Dictionary with test results
        """
        logger.info("Running drift tests...")
        
        # Create test suite
        test_suite = TestSuite(tests=[
            TestNumberOfColumns(),
            TestNumberOfRows(),
            TestColumnsType(),
            TestNumberOfDriftedColumns(lt=5),  # Less than 5 drifted columns
            TestShareOfDriftedColumns(lt=0.3),  # Less than 30% drifted
        ])
        
        # Run tests
        test_suite.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )
        
        # Save test results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = self.output_dir / f"drift_tests_{timestamp}.html"
        test_suite.save_html(str(html_path))
        
        # Get test results
        test_results = test_suite.as_dict()
        
        # Check if all tests passed
        all_passed = all(
            test['status'] == 'SUCCESS' 
            for test in test_results.get('tests', [])
        )
        
        return {
            'all_tests_passed': all_passed,
            'timestamp': timestamp,
            'test_results': test_results,
            'report_path': str(html_path)
        }
    
    def _extract_drift_summary(self, report_json: Dict) -> Dict:
        """Extract key drift metrics from report JSON."""
        try:
            metrics = report_json.get('metrics', [])
            
            summary = {
                'timestamp': datetime.now().isoformat(),
                'dataset_drift_detected': False,
                'number_of_drifted_columns': 0,
                'share_of_drifted_columns': 0.0,
                'drifted_features': []
            }
            
            # Extract dataset drift metric
            for metric in metrics:
                metric_type = metric.get('metric', '')
                
                if 'DatasetDriftMetric' in metric_type:
                    result = metric.get('result', {})
                    summary['dataset_drift_detected'] = result.get('dataset_drift', False)
                    summary['number_of_drifted_columns'] = result.get('number_of_drifted_columns', 0)
                    summary['share_of_drifted_columns'] = result.get('share_of_drifted_columns', 0.0)
                    
                    # Get list of drifted features
                    drift_by_columns = result.get('drift_by_columns', {})
                    summary['drifted_features'] = [
                        col for col, info in drift_by_columns.items()
                        if info.get('drift_detected', False)
                    ]
            
            return summary
            
        except Exception as e:
            logger.error(f"Error extracting drift summary: {e}")
            return {'error': str(e)}
    
    def check_drift_alert(self, drift_summary: Dict, threshold: float = 0.3) -> bool:
        """
        Check if drift exceeds threshold and should trigger alert.
        
        Args:
            drift_summary: Drift summary from generate_drift_report
            threshold: Maximum acceptable share of drifted columns
            
        Returns:
            True if alert should be triggered
        """
        share_drifted = drift_summary.get('share_of_drifted_columns', 0)
        dataset_drift = drift_summary.get('dataset_drift_detected', False)
        
        should_alert = share_drifted > threshold or dataset_drift
        
        if should_alert:
            logger.warning(
                f"DRIFT ALERT: {share_drifted*100:.1f}% of columns drifted. "
                f"Drifted features: {drift_summary.get('drifted_features', [])}"
            )
        
        return should_alert


def monitor_production_data(
    current_data_path: str,
    reference_data_path: str = "data/processed/train.csv",
    output_dir: str = "reports/drift"
) -> Dict:
    """
    Convenience function to monitor production data.
    
    Args:
        current_data_path: Path to current production data
        reference_data_path: Path to reference training data
        output_dir: Output directory for reports
        
    Returns:
        Drift summary with alert status
    """
    # Initialize monitor
    monitor = DriftMonitor(reference_data_path, output_dir)
    
    # Load current data
    current_data = pd.read_csv(current_data_path)
    logger.info(f"Loaded current data: {len(current_data)} rows")
    
    # Generate drift report
    drift_summary = monitor.generate_drift_report(current_data)
    
    # Run tests
    test_results = monitor.run_drift_tests(current_data)
    drift_summary['tests_passed'] = test_results['all_tests_passed']
    
    # Check if alert needed
    drift_summary['alert_triggered'] = monitor.check_drift_alert(drift_summary)
    
    return drift_summary


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Monitor drift using validation data as "current" data
    # (In production, this would be actual production data)
    summary = monitor_production_data(
        current_data_path="data/processed/val.csv",
        reference_data_path="data/processed/train.csv"
    )
    
    print("\n" + "="*70)
    print("DRIFT MONITORING SUMMARY")
    print("="*70)
    print(f"Dataset drift detected: {summary['dataset_drift_detected']}")
    print(f"Drifted columns: {summary['number_of_drifted_columns']}")
    print(f"Share drifted: {summary['share_of_drifted_columns']*100:.1f}%")
    print(f"Drifted features: {summary['drifted_features']}")
    print(f"All tests passed: {summary['tests_passed']}")
    print(f"Alert triggered: {summary['alert_triggered']}")
    print("="*70)

