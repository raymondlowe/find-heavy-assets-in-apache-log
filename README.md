# find-heavy-assets-in-apache-log
Scan an apache web server log, in default CPanel format, and report on the assets that are heaviest using bandwidth and slowing down pages

## usage

Usage: find-heavy-assets.py [--verbose] [--help] <apache log file>
--verbose or -v: print verbose output
--help or -h: print this help message
<apache log file>: apache log file to process
output will be a spreadsheet in the current directory called heavy_assets.xlsx
  
  
## Caution
  
  Byte sizes are from the apache logs but if compression is done somewhere else, such as cloudflare, then the size received by the browser may be (much) smaller.
  
  Figures for uncompressable things like images will be acurate, but figures for highly compressable things like css and to a lesser extend js may be wrong.
  
