#!/usr/bin/env python3
"""
Daily Stock Analysis - Main Entry Point

This module serves as the primary entry point for the daily stock analysis tool.
It orchestrates data fetching, analysis, and report generation.
"""

import os
import sys
import logging
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/stock_analysis_{datetime.now().strftime('%Y%m%d')}.log"),
    ],
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Daily Stock Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --symbols AAPL MSFT GOOGL
  python main.py --symbols TSLA --date 2024-01-15
  python main.py --symbols AAPL --output-format json
        """,
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        required=False,
        default=os.getenv("DEFAULT_SYMBOLS", "AAPL,MSFT,GOOGL").split(","),
        help="Stock ticker symbols to analyze (e.g., AAPL MSFT GOOGL)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Analysis date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=int(os.getenv("LOOKBACK_DAYS", 30)),
        help="Number of historical days to include in analysis (default: 30)",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "csv", "html", "console"],
        default=os.getenv("OUTPUT_FORMAT", "console"),
        help="Output format for the analysis report",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=os.getenv("OUTPUT_DIR", "reports"),
        help="Directory to save output reports",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose/debug logging",
    )
    return parser.parse_args()


def setup_directories(output_dir: str) -> None:
    """Ensure required directories exist."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    logger.debug("Directories initialized: logs/, %s/", output_dir)


def resolve_analysis_date(date_str: str | None) -> datetime:
    """Resolve the target analysis date."""
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            logger.error("Invalid date format '%s'. Expected YYYY-MM-DD.", date_str)
            sys.exit(1)
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def main() -> int:
    """Main execution function.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    setup_directories(args.output_dir)

    analysis_date = resolve_analysis_date(args.date)
    start_date = analysis_date - timedelta(days=args.lookback_days)

    logger.info("=" * 60)
    logger.info("Daily Stock Analysis")
    logger.info("=" * 60)
    logger.info("Analysis Date : %s", analysis_date.strftime("%Y-%m-%d"))
    logger.info("Lookback Period: %d days (%s to %s)",
                args.lookback_days,
                start_date.strftime("%Y-%m-%d"),
                analysis_date.strftime("%Y-%m-%d"))
    logger.info("Symbols       : %s", ", ".join(args.symbols))
    logger.info("Output Format : %s", args.output_format)
    logger.info("Output Dir    : %s", args.output_dir)
    logger.info("=" * 60)

    # TODO: Wire in fetcher, analyzer, and reporter modules as they are built
    logger.info("Analysis pipeline initialized. Modules pending implementation.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
