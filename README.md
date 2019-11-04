# Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data
This repo contains all the codes and sample files for the "Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data" paper 

## Short-term Pattern Discovery
Short-term or propagation patterns are those which show the impact of geo-spatiotemporal entities/events on a sequential basis, where one entity can be propagated and cause other entities to happen. One example is a _rain_ event which causes a _traffic accident_, and the _accident_ causes _traffic congestion_. 

## Long-term Pattern Discovery
Long-term or influential patters are those which show the impact of a temporally long geo-spatiotemporal entity on its spatial neighborhood. One example is a _major construction_ which causes more _traffic jams_ in its spatial neighborhood. 

## Requirements 
The only requirement is ```Python```, version 2.7 is recommended.

## Data Pre-processing Steps
Prior to performing any pattern extraction on traffic and weather data (as examples of geo-spatiotemporal data), there are two main pre-processing steps: 
  * __Extracting Events/Entities__: The first step is to extract traffic and weather events/entities from the raw traffic and weather data, and create a dataset such as [Large-Scale Traffic and Weather Events Dataset](https://smoosavi.org/datasets/lstw). In ```short-term/0-CreateMixtureEventFile.py```, you see a variety of processes, and empirically driven thresholds and settings to extract each type of traffic or weather event/entity. 
  * __Removing Redundant Traffic Events__: The second step is to remove duplicated geo-spatiotemporal entities/events using ```short-term/1-RemoveRedundantTrafficEvents.py```. 
 
## How to Run
* __Extracting Short-term Patterns__: there are multiple steps to extract short-term patterns as follows:
  * __Finding Child-Parent Relations__: Before building relation trees, we need to find the child-parent relationship between every two geo-spatiotemporal entities. Use ```short-term/2-FindChildsParents.py``` to perform this step. 
  * __Creating Sequences of Relations__: This step is also before building relation trees, which creates sequences of relations between geo-spatiotemporal entities using ```short-term/3-FindSequencesOfPatterns.py```. 
  * __Extracting Tree Structures from Sequences__: This step creates relation trees based on previously extracted sequences of relations using ```short-term/4-ExtractTreesFromSequences.py```. 
  * __Mining Frequent Tree Patterns__: Finally, this step extracts frequent embedded unordered tree patterns from a forest of relation trees using ```short-term/5-FindFrequentTreePatterns_revised_City.py```, which is based on [SELUTH](http://www.cs.rpi.edu/~zaki/www-new/pmwiki.php/Software/Software#sleuth) algorithm proposed by [Zaki 2005](http://www.cs.rpi.edu/~zaki/PaperDir/FI05.pdf). 


* __Extracting Long-term Patterns__:


## Dataset
A large-scale dataset of traffic and weather event data is used as input. Check [here](https://smoosavi.org/datasets/lstw) for the latest version of such a dataset. The data comes in the form of a single CSV file. We use the same data as input to both short and long-term pattern discovery processes. 


<!-- ## Sample Results -->


## Acknowledgment
* Moosavi, Sobhan, Mohammad Hossein Samavatian, Arnab Nandi, Srinivasan Parthasarathy, and Rajiv Ramnath. ["Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data."](https://arxiv.org/abs/1902.06792) Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. ACM, 2019. 

```
@article{moosavi2019short,
  title={Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data},
  author={Moosavi, Sobhan and Samavatian, Mohammad Hossein and Nandi, Arnab and Parthasarathy, Srinivasan and Ramnath, Rajiv},
  booktitle = {Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery \&\#38; Data Mining},
  year = {2019},
  isbn = {978-1-4503-6201-6},
  location = {Anchorage, AK, USA},
  pages = {2905--2913},
  doi = {10.1145/3292500.3330755},  
  publisher = {ACM},
  address = {New York, NY, USA}
}
```
