# slrtool
Tool for Performing Systematic Literature Review 

This tool allows for speeding up the process of applying inclusion/exclusion criteria when querying and filtering articles
for performing a Systematic Review of the Literature. Also, allows others to repeat the same query, following the same
criteria you defined in your paper.


### How to use

#### ./search.py

Select an action

(1) Search link
(2) Generate LaTex code
(3) Download raw list of articles from a source
(4) Apply exclusion criteria to the articles
(5) Generate list of excluded DOI between auto-filtered and manual-filtered


1. Search link 

Build the URL for the article source

2. Generate LaTex code

Generates a table in LaTex for all of the sources with the search links to put on your report

3.  Download raw list of articles from a source

Tries to download all of the html and process them to build a CSV file with title, description (from the abstract), DOI and url

4.  Apply exclusion criteria to the articles

Apply criteria for inclusion (include only articles that contain some strings on it's title / abstract) an exclusion (exclude articles that contain some strings on it's title / abstract)

5. Generate list of excluded DOI between auto-filtered and manual-filtered

After applying the exclusion and inclusion criteria, we often find some, if not many, unrelated articles. Therefore, it is important to be able to exclude them from future filters. So this option is used to compare the auto-filtered with the manually excluded articles and generates a file with the missing DOI. Those DOI codes can be 
included in the filter_config.json, on the "remove_doi": [ ] property, for being auto excluded in the future.