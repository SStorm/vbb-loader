# Roman's Crate VBB schema loader

## Usage

1. Start an instance of crate with:

```
docker run -p "4200:4200" -p 5432:5432 crate
```
 
2. Download the VBB transit dataset and put it in some folder (unzipped), my folder looks like this:

```
➜  coding-assignment ls -lh
total 398M
-rw-rw-r-- 1 romanas romanas 3.6K Oct 15 18:36 agency.txt
-rw-rw-r-- 1 romanas romanas  50M Oct 20 14:06 BVG_VBB_bereichsscharf.zip
-rw-rw-r-- 1 romanas romanas 197K Oct 15 18:36 calendar_dates.txt
-rw-rw-r-- 1 romanas romanas  63K Oct 15 18:36 calendar.txt
-rw-rw-r-- 1 romanas romanas   64 Oct 15 18:28 frequencies.txt
-rw-rw-r-- 1 romanas romanas  140 Oct 15 18:28 pathways.txt
-rw-rw-r-- 1 romanas romanas  49K Oct 15 18:36 routes.txt
-rw-rw-r-- 1 romanas romanas 125M Oct 15 18:36 shapes.txt
-rw-rw-r-- 1 romanas romanas 4.6M Oct 15 18:36 stops.txt
-rw-rw-r-- 1 romanas romanas 205M Oct 22 22:24 stop_times.txt
-rw-rw-r-- 1 romanas romanas 4.2M Oct 15 18:36 transfers.txt
-rw-rw-r-- 1 romanas romanas  11M Oct 15 18:36 trips.txt
```

3. Create a venv and install the dependencies. I have tested this with Python 3.8, others might work too.

```
python -m venv venv
pip install -r requirements.txt
```

4. Loading the entire folder where the dataset is is then a matter of these two commands:

```
python -m vbb_loader.schema.init "http://localhost:4200" "crate" ""
python -m vbb_loader.loader.load_dir ~/path-to-vbb-dir/ "http://localhost:4200" "crate" ""
```
    
The output should be something like:

```    
(venv) ➜  vbb-loader git:(master) ✗ python -m vbb_loader.loader.load_dir ~/work/crate/coding-assignment/ "http://localhost:4200" "crate" ""
2020-10-22 23:43:22,779 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:43:22,783 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:43:22,783 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/stop_times.txt' to table 'vbb_stop_times'
2020-10-22 23:47:20,735 [TableLoader                     ] [INFO    ] - Loaded 3575943 rows
2020-10-22 23:47:20,735 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:20,737 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:20,738 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/trips.txt' to table 'vbb_trips'
2020-10-22 23:47:33,179 [TableLoader                     ] [INFO    ] - Loaded 173919 rows
2020-10-22 23:47:33,179 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:33,182 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:33,182 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/calendar.txt' to table 'vbb_calendar'
2020-10-22 23:47:33,409 [TableLoader                     ] [INFO    ] - Loaded 1698 rows
2020-10-22 23:47:33,409 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:33,411 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:33,411 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/stops.txt' to table 'vbb_stops'
2020-10-22 23:47:36,594 [TableLoader                     ] [INFO    ] - Loaded 41594 rows
2020-10-22 23:47:36,595 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:36,597 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:36,597 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/routes.txt' to table 'vbb_routes'
2020-10-22 23:47:36,670 [TableLoader                     ] [INFO    ] - Loaded 1299 rows
2020-10-22 23:47:36,670 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:36,673 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:36,673 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/calendar_dates.txt' to table 'vbb_calendar_dates'
2020-10-22 23:47:37,365 [TableLoader                     ] [INFO    ] - Loaded 12239 rows
2020-10-22 23:47:37,366 [__main__                        ] [WARNING ] - No such table for file frequencies.txt
2020-10-22 23:47:37,366 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:37,368 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:37,368 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/transfers.txt' to table 'vbb_transfers'
2020-10-22 23:47:44,030 [TableLoader                     ] [INFO    ] - Loaded 105177 rows
2020-10-22 23:47:44,030 [__main__                        ] [WARNING ] - No such table for file pathways.txt
2020-10-22 23:47:44,030 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:44,033 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:44,033 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/agency.txt' to table 'vbb_agency'
2020-10-22 23:47:44,037 [TableLoader                     ] [INFO    ] - Loaded 38 rows
2020-10-22 23:47:44,037 [vbb_loader.client.db_client     ] [INFO    ] - Will connect to CrateDB at 'http://localhost:4200' ...
2020-10-22 23:47:44,040 [vbb_loader.client.db_client     ] [INFO    ] - Success
2020-10-22 23:47:44,040 [TableLoader                     ] [INFO    ] - Will load file '/home/romanas/work/crate/coding-assignment/shapes.txt' to table 'vbb_shapes'
2020-10-22 23:48:32,753 [TableLoader                     ] [INFO    ] - Loaded 13752 rows
2020-10-22 23:48:32,753 [__main__                        ] [INFO    ] - Done
```
    
Note that schema initialization will always nuke the database...

## Explanation of approach

This seemed like a classic piece of ETL. I initially attempted to use the PostgreSQL python libraries
to connect to crate that way, but had no success due to various errors connecting and gave up after an hour.
Then proceeded to use the official crate client lib, which worked fine. 

Schema creation is done in vbb_loader/schema/init.py, which is a simple script that loads and executes schema.sql. 
It doesn't attempt to be very smart and splits by ';', which is sufficient in this simple case.

Loading is then done in vbb_loader/loader/load_file.py. Since all the files are pretty simple and similar, it all follows the same pattern. 
I wrote a set of transformers to adjust the data on a per-table basis. This is primarily used in the shapes and stops, which have geo points and geo shapes. 
I also used transformers to adjust the types of some of the fields, because the default Python CSV parser doesn't do type inference. 
There is probably a nicer way to do this, but I was running up against the 4hr limit and took the easy way out here...

Inserts are done in batches, the size of which is controlled by the BATCH_SIZE constant in load_file.py.

I have ignored frequencies.txt and pathways.txt because they are empty files, hope that is OK. 

The loading process for the entire dataset takes about 5 minutes with a batch size of 100, and about 2 minutes with a batch size of 1000. 
This can probably be tweaked further, but I'd need to delve deeper into what are the best practices with crate.

I chose not to write any unit tests for this, as it is a simple ETL app and it's easy to test it with the dataset itself - 
not clear what the benefit of unit tests would be in this particular case. 

In total I spent about 5-6hrs on this, of which about 1hr was spent attempting to use Crate as Postgres, which proved futile. 

This has been tested on Linux and macOS, I hope you won't try it on Windows because I have no idea what might happen! :)

In general, I found the geo_shape stuff to be the most interesting, as I haven't done anything with geo data before. 
This was also trickiest to get right and took quite a few attempts before it worked correctly (I think). 
Even though you can click on the shape in the crate GUI and it takes you to geojson.io, that fails to parse - I suspect it might be an issue with crate rather than the data?
Because Crate is not super popular, it's generally more difficult to find answers to questions online, so there was a lot of trial and error.

In any case, regardless of how this goes ahead, this was fun and I thank you for the challenge :)
