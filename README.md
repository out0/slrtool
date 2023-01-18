# slrtool
Tool for Performing Systematic Literature Review 

This tool allows for speeding up the process of applying inclusion/exclusion criteria when querying and filtering articles
for performing a Systematic Review of the Literature. Also, allows others to repeat the same query, following the same
criteria you defined in your paper.


### How to use

#### ./search.py
<br />
Select an action<br />
<br />
(1) Search link<br />
(2) Generate LaTex code<br />
(3) Download raw list of articles from a source<br />
(4) Apply exclusion criteria to the articles<br />
(5) Generate list of excluded DOI between auto-filtered and manual-filtered<br />
<br />

1. Search link: <br />
Builds the URL for the article source<br />
2. Generate LaTex code:<br />
Generates a table in LaTex for all of the sources with the search links to put on your report<br />
3.  Download raw list of articles from a source:<br />
Tries to download all of the html and process them to build a CSV file with title, description (from the abstract), DOI and url<br />
4.  Apply exclusion criteria to the articles:<br />
Apply criteria for inclusion (include only articles that contain some strings on it's title / abstract) an exclusion (exclude articles that contain some strings on it's title / abstract)<br />
5. Generate list of excluded DOI between auto-filtered and manual-filtered:<br />
After applying the exclusion and inclusion criteria, we often find some, if not many, unrelated articles. Therefore, it is important to be able to exclude them from future filters. So this option is used to compare the auto-filtered with the manually excluded articles and generates a file with the missing DOI. Those DOI codes can be included in the filter_config.json, on the "remove_doi": [ ] property, for being auto excluded in the future.<br />
