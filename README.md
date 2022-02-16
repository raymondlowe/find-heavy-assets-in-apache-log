# find-heavy-assets-in-apache-log
Scan an apache web server log, in default CPanel format, and report on the assets that are heaviest using bandwidth and slowing down pages

## usage

Usage: find-heavy-assets.py [--verbose] [--help] <apache log file>
--verbose or -v: print verbose output
--help or -h: print this help message
<apache log file>: apache log file to process
output will be a spreadsheet in the current directory called heavy_assets.xlsx
  
  
