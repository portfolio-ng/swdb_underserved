Simple script to determine which locations in a region are farthest from a natural water source.

#### SWDB
The USGS released a database called the Shuttle Radar Topography Mission Water Body Data, SWDB.
The SWDB is a database of ESRI Shapefiles simplified to be effectively a bitmap of land and water.

This is a test environment script to mimic the use with the SWDB data.

Built to aide an NGO I work with to identify and target communities most underserved by natural water sources.

#### Directory Tree
* dada/ : directory containing the faux bitmap data.
* scripts : directory containing the scripts.
  * magn.py : support library for underserved.py that calculates the unique slopes to search along.
  * underserved.py : searches for watersources in a bitmapped GIS shapefile.
  * plae_analysis : was unable to help myself, once I collected the unique slopes I needed to know if there was a pattern to each successive magnitude.

### Example Usage:
```bash
./underserved.py -l 16,16
  branch magnitude: 4
  dims: 16 , 16
mat:

 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 1
 0 0 0 0 0 0 0 1 1 1 1 0 1 1 1 1
 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
und_mat:

  5  5  4  4  4  4  4  5  5  5  6  6  5  5  5  5
  5  4  3  3  3  3  3  4  4  5  5  5  5  4  4  4
  4  3  2  2  2  2  2  3  3  4  4  4  4  3  3  3
  4  3  2  1  1  1  2  2  2  3  3  3  3  2  2  2
  4  3  2  1  0  1  1  1  2  2  2  2  2  2  1  1
  4  3  2  1  1  0  0  1  1  1  1  1  1  1  1  0
  4  3  2  2  1  1  1  0  0  0  0  1  0  0  0  0
  5  4  3  2  2  2  1  1  1  1  0  0  0  0  0  0
  5  5  4  3  3  2  2  2  2  1  1  1  1  1  0  0
  6  5  5  4  4  3  3  3  2  2  2  2  2  1  1  1
  7  6  5  5  5  4  4  4  3  3  3  3  2  2  2  2
  8  7  6  6  5  5  5  5  4  4  4  4  3  3  3  3
  8  8  8  7  6  6  6  5  5  5  5  5  4  4  4  4
  9  8  8  8  8  8  7  6  6  6  6  5  5  5  5  5
 10 10  9  8  8  8  8  8  8  8  7  6  6  6  6  6
 11 10 10 10  9  9  8  8  8  8  8  8  8  8  7  7

```

The -l argument limits the faux data.

The first matrix is the faux data; with 0s representing land and 1s representing water.

The second matrix takes the shortest distance from a position to a water source and stores it as an integer value.  Note: 0s in the second matrix are water due to the distance to water being 0 at a water source..

#### Some Internals
The number of branching paths to search is determined by the branch magnitude variable in onit().

magn.py uses this variable to determine a matrix around the point outward this value.

branch_magn=4 will result in a matrix like this:

```python
  3 3 3 3 3 3 3
  3 2 2 2 2 2 3
  3 2 1 1 1 2 3 
  3 2 1 0 1 2 3
  3 2 1 1 1 2 3
  3 2 2 2 2 2 3  
  3 3 3 3 3 3 3
```

Then magn.py determines any redundant slopes in regards to each element's location, but only for the area between x=0 and y=x.

```python
  _ _ _ _ _ _ 0
  _ _ _ _ _ 0 3
  _ _ _ _ 1 2 3 
  _ _ _ 0 1 0 0
  _ _ _ _ _ _ _
  _ _ _ _ _ _ _  
  _ _ _ _ _ _ _
```

Then it applies the necessary rotations to remove any redudant slopes in all directions.

```python
 0 3 3 0 3 3 0
 3 0 2 0 2 0 3
 3 2 1 1 1 2 3
 0 0 1 0 1 0 0
 3 2 1 1 1 2 3
 3 0 2 0 2 0 3
 0 3 3 0 3 3 0
```
The remaining unique slope vectors are used to determine which direction the nearest water source may be.
