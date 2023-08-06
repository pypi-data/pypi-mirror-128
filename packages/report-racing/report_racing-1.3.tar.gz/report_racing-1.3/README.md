# Report of Monaco 2018 Racing
### This package accepts data files as input and forms the standings of the riders
## Getting started
### The program receives files as input, processes them and passes them to the script.
###### Files that the program accepts
``` 
    start = list(arguments.files.glob('start.log')).pop()
    end = list(arguments.files.glob('end.log')).pop() 
    abbreviations = list(arguments.files.glob('abbreviations.txt')).pop() 
```
###### Arguments for working with a script
```
    parser.add_argument('--files', type=pathlib.Path, required=True)
    parser.add_argument('--asc', action='store_true')
    parser.add_argument('--desc', action='store_true')
    parser.add_argument('--driver', type=str)
```
### Function parse_files
> The function reads input files, adds data to a dictionary
---
###### start, end, abbreviations - object witch is the result of parser.parse_args()

###### Returns a dictionary with ordered data about the riders
### Function build_report
> The function reads out the lap time and sorts the riders according to it. The default is ascending time.
---
###### pilots - driver data dictionary
###### reverse=False - default sort value

###### Returns an ordered list with member abbreviations
### Function print_report
> Forms the standings, taking into account the conditions of the problem
---
###### abbr_racer - list with riders abbreviations

###### Returns standings with racers