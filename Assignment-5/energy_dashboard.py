import logging
from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------
# Data Ingestion & Cleaning
# -----------------------------

def ingest_data(data_dir: Path) -> pd.DataFrame:
    """
    Ingests all CSV files from the provided data directory, cleans them,
    and returns a combined pandas DataFrame indexed by Timestamp.

    - Uses pathlib to find .csv files
    - Uses pandas.read_csv with on_bad_lines='skip'
    - Converts 'Timestamp' to datetime and sets as index
    - Logs and skips files that error
    """
    all_rows = []

    if not data_dir.exists():
        logger.error("Data directory does not exist: %s", data_dir)
        return pd.DataFrame()

    csv_files = sorted(data_dir.glob("*.csv"))
    if not csv_files:
        logger.warning("No CSV files found in data directory: %s", data_dir)

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, on_bad_lines='skip')
            # Expect columns: Timestamp, Building, kWh
            if 'Timestamp' not in df.columns:
                logger.warning("Missing 'Timestamp' column in %s; skipping.", csv_file)
                continue
            if 'Building' not in df.columns:
                logger.warning("Missing 'Building' column in %s; skipping.", csv_file)
                continue
            if 'kWh' not in df.columns:
                logger.warning("Missing 'kWh' column in %s; skipping.", csv_file)
                continue

            # Convert Timestamp
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df = df.dropna(subset=['Timestamp'])
            df = df.sort_values('Timestamp')
            all_rows.append(df)
            logger.info("Ingested %s with %d rows.", csv_file.name, len(df))
        except FileNotFoundError:
            logger.exception("File not found: %s", csv_file)
            continue
        except Exception:
            logger.exception("Error reading file: %s", csv_file)
            continue

    if not all_rows:
        logger.warning("No valid data ingested.")
        return pd.DataFrame()

    df_combined = pd.concat(all_rows, ignore_index=True)
    df_combined = df_combined.set_index('Timestamp')

    # Ensure kWh numeric
    df_combined['kWh'] = pd.to_numeric(df_combined['kWh'], errors='coerce')
    df_combined = df_combined.dropna(subset=['kWh'])

    return df_combined


# -----------------------------
# Object-Oriented Modeling & Aggregation
# -----------------------------

class BuildingManager:
    def __init__(self, df_combined: pd.DataFrame):
        self.df = df_combined.copy()
        self.summary_stats: Optional[pd.DataFrame] = None
        self.daily_totals: Optional[pd.DataFrame] = None
        self.weekly_avg_by_building: Optional[pd.DataFrame] = None
        self.peak_hours_by_building: Optional[pd.DataFrame] = None

    def calculate_summary_statistics(self) -> pd.DataFrame:
        """
        Group by Building and compute mean, min, max, and sum of kWh.
        """
        if self.df.empty:
            logger.warning("DataFrame is empty; cannot compute summary statistics.")
            self.summary_stats = pd.DataFrame()
            return self.summary_stats

        grouped = self.df.groupby('Building')['kWh']
        self.summary_stats = grouped.agg(
            mean_kWh='mean',
            min_kWh='min',
            max_kWh='max',
            total_kWh='sum'
        ).sort_values('total_kWh', ascending=False)
        logger.info("Calculated summary statistics for %d buildings.", len(self.summary_stats))
        return self.summary_stats

    def calculate_time_trends(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        - Daily campus totals using resample('D') on the full dataset
        - Average weekly usage per building via groupby + resample
        """
        if self.df.empty:
            logger.warning("DataFrame is empty; cannot compute time trends.")
            self.daily_totals = pd.DataFrame()
            self.weekly_avg_by_building = pd.DataFrame()
            return self.daily_totals, self.weekly_avg_by_building

        # Daily campus totals
        self.daily_totals = self.df['kWh'].resample('D').sum()

        # Weekly average usage per building
        weekly = self.df.groupby('Building')['kWh'].resample('W').mean()
        # Convert to wide format for plotting bars per building
        self.weekly_avg_by_building = weekly.unstack(level=0)
        logger.info("Computed daily totals (%d days) and weekly averages.", len(self.daily_totals))

        # Peak hours per building (proxy): hour-of-day vs max usage
        df_with_hour = self.df.copy()
        df_with_hour['Hour'] = df_with_hour.index.hour
        self.peak_hours_by_building = df_with_hour.groupby('Building').apply(
            lambda g: g.loc[g['kWh'].idxmax()][['Hour', 'kWh']]
        )
        self.peak_hours_by_building.columns = ['PeakHour', 'Peak_kWh']
        return self.daily_totals, self.weekly_avg_by_building

    def generate_dashboard_plots(self, output_path: Path) -> Path:
        """
        Creates a 4-panel figure with:
        - Trend Line: Daily consumption over time
        - Bar Chart: Average weekly usage across buildings
        - Scatter Plot: Peak consumption times (hour-of-day vs max usage)
        Saves as dashboard.png
        """
        if self.daily_totals is None or self.weekly_avg_by_building is None:
            # Ensure trends are calculated
            self.calculate_time_trends()

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        ax1, ax2 = axes[0]
        ax3, ax4 = axes[1]

        # Panel 1: Daily Trend Line (Campus total)
        if isinstance(self.daily_totals, pd.Series) and not self.daily_totals.empty:
            ax1.plot(self.daily_totals.index, self.daily_totals.values, label='Daily Total kWh', color='tab:blue')
            ax1.set_title('Daily Campus Energy Consumption')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('kWh')
            ax1.legend()
        else:
            ax1.text(0.5, 0.5, 'No Daily Data', ha='center', va='center')
            ax1.set_title('Daily Campus Energy Consumption')

        # Panel 2: Weekly Average Bar Chart (Buildings)
        if isinstance(self.weekly_avg_by_building, pd.DataFrame) and not self.weekly_avg_by_building.empty:
            # Compute overall average across weeks for each building
            avg_weekly = self.weekly_avg_by_building.mean(axis=0)
            avg_weekly.sort_values(ascending=False).plot(kind='bar', ax=ax2, color='tab:orange')
            ax2.set_title('Average Weekly Usage by Building')
            ax2.set_xlabel('Building')
            ax2.set_ylabel('Average Weekly kWh')
        else:
            ax2.text(0.5, 0.5, 'No Weekly Data', ha='center', va='center')
            ax2.set_title('Average Weekly Usage by Building')

        # Panel 3: Scatter Plot of Peak Hours vs Peak kWh per Building
        if isinstance(self.peak_hours_by_building, pd.DataFrame) and not self.peak_hours_by_building.empty:
            ax3.scatter(self.peak_hours_by_building['PeakHour'], self.peak_hours_by_building['Peak_kWh'], color='tab:green')
            for b, row in self.peak_hours_by_building.iterrows():
                ax3.annotate(str(b), (row['PeakHour'], row['Peak_kWh']))
            ax3.set_title('Peak Hour vs Peak kWh (per Building)')
            ax3.set_xlabel('Hour of Day')
            ax3.set_ylabel('Peak kWh')
            ax3.set_xticks(range(0, 24, 2))
        else:
            ax3.text(0.5, 0.5, 'No Peak Data', ha='center', va='center')
            ax3.set_title('Peak Hour vs Peak kWh (per Building)')

        # Panel 4: Spare panel for future metrics or a simple table-like text
        ax4.axis('off')
        ax4.text(0.01, 0.95, 'Executive Summary', fontsize=12, fontweight='bold')
        if self.summary_stats is not None and not self.summary_stats.empty:
            total_consumption = self.summary_stats['total_kWh'].sum()
            top_building = self.summary_stats['total_kWh'].idxmax()
            top_building_value = self.summary_stats.loc[top_building, 'total_kWh']
            peak_desc = 'Varies by building (see scatter)'
            main_trend = 'Campus shows daily variability with weekly patterns.'
            lines = [
                f"Total campus consumption: {total_consumption:,.0f} kWh",
                f"Highest-consuming building: {top_building} ({top_building_value:,.0f} kWh)",
                f"Peak load time: {peak_desc}",
                f"Main trend: {main_trend}",
            ]
            ax4.text(0.01, 0.85, "\n".join(lines), fontsize=10, va='top')
        else:
            ax4.text(0.01, 0.85, 'No summary available.', fontsize=10, va='top')

        fig.tight_layout()
        output_file = output_path / 'dashboard.png'
        fig.savefig(output_file, dpi=150)
        plt.close(fig)
        logger.info("Saved dashboard plot to %s", output_file)
        return output_file

    def export_results(self, output_path: Path) -> Path:
        """
        Exports building summary statistics to CSV and prints an Executive Summary.
        """
        if self.summary_stats is None:
            self.calculate_summary_statistics()

        output_csv = output_path / 'building_summary.csv'
        if self.summary_stats is not None:
            self.summary_stats.to_csv(output_csv)
            logger.info("Exported building summary to %s", output_csv)

        # Print Executive Summary (minimum 4 lines)
        if self.summary_stats is not None and not self.summary_stats.empty:
            total_consumption = self.summary_stats['total_kWh'].sum()
            highest_building = self.summary_stats['total_kWh'].idxmax()
            highest_value = self.summary_stats.loc[highest_building, 'total_kWh']

            peak_time_desc = 'Peak hour varies by building; see dashboard scatter.'
            main_trend_desc = 'Daily totals fluctuate; weekly averages highlight building usage.'

            print("Executive Summary")
            print("- Total campus consumption:", f"{total_consumption:,.0f} kWh")
            print("- Highest-consuming building:", f"{highest_building} ({highest_value:,.0f} kWh)")
            print("- Peak load time:", peak_time_desc)
            print("- Main trend:", main_trend_desc)
        else:
            print("Executive Summary")
            print("- No data available for summary.")
            print("- Ensure CSVs contain Timestamp, Building, kWh.")
            print("- Re-run after adding valid data.")
            print("- Dashboard will show placeholders if data is missing.")

        return output_csv


# -----------------------------
# Main execution pipeline
# -----------------------------

def _simulate_data(output_dir: Path) -> Path:
    """Create a simulated /data directory with example CSVs for demonstration."""
    data_dir = output_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    # Simulate three buildings with 30 days of hourly data
    rng = pd.date_range(end=pd.Timestamp.today().normalize(), periods=30*24, freq='H')
    buildings = ['Library', 'Engineering', 'Hostel']

    for b in buildings:
        df = pd.DataFrame({
            'Timestamp': rng,
            'Building': b,
            'kWh': (
                50
                + 10 * pd.Series(range(len(rng))) % 24  # small daily pattern
                + (10 if b == 'Engineering' else 0)     # baseline difference
                + (5 if b == 'Hostel' else 0)
            )
        })
        # Add mild random variation
        df['kWh'] = df['kWh'] + pd.Series(np.random.default_rng(42).normal(0, 3, size=len(df)))

        file_path = data_dir / f"{b.lower()}_energy.csv"
        df.to_csv(file_path, index=False)
    logger.info("Simulated data written to %s", data_dir)
    return data_dir


def main():
    base_dir = Path(__file__).parent
    output_dir = base_dir

    # Prefer real data if present; else simulate
    data_dir = output_dir / 'data'
    if not data_dir.exists() or not list(data_dir.glob('*.csv')):
        logger.info("No data found; generating simulated data...")
        data_dir = _simulate_data(output_dir)

    df = ingest_data(data_dir)
    manager = BuildingManager(df)

    # Compute stats and trends
    manager.calculate_summary_statistics()
    manager.calculate_time_trends()

    # Generate dashboard plots
    manager.generate_dashboard_plots(output_dir)

    # Export results and print executive summary
    manager.export_results(output_dir)


if __name__ == '__main__':
    main()