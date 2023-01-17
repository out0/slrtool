from io import StringIO

from sources.ArticleSource import *
from sources.SourceAcm import *
from sources.SourceIEEE import *
from sources.SourceScienceDirect import *
from sources.SourceSpringer import *
from sources.SourceWiley import *

from util.HtmlParser import *
from model.Article import *


class LatexBuilder:

    def __build_source_row(strb:StringIO, source: ArticleSource, terms: dict):
        result = source.buildSearchLink(terms)
        strb.write(
            f"{result.source_name} & {result.search_query} & 0 & 0 \\\\ \n")
        strb.write("\hline\n")
        

    def build_latex(conf: dict) -> None:
        strb = StringIO()
        terms = conf["queries"]
        #[all, count_files] = count_selected_articles_by_source(conf)

        strb.write("% -----------------------------\n")
        strb.write("% Search terms table code BEGIN\n")
        strb.write("% -----------------------------\n")
        strb.write("\\begin{table}[h]\n")
        strb.write("\centering\n")
        strb.write("%\\renewcommand\\arraystretch{1.5}\n")
        strb.write("\\begin{tabular}{|C|P{8cm}|c|c|c|}\n\hline\n")
        strb.write(
            "\\textbf{Location} & \\textbf{Search String} & \\textbf{Result Quantity} \\\\ \n")
        strb.write("\hline\n")

        LatexBuilder.__build_source_row(strb, SourceAcm(), terms["acm"])
        LatexBuilder.__build_source_row(strb, SourceIEEE(), terms["ieee"])
        LatexBuilder.__build_source_row(strb, SourceScienceDirect(), terms["science"])
        LatexBuilder.__build_source_row(strb, SourceSpringer(), terms["springer"])
        LatexBuilder.__build_source_row(strb, SourceWiley(), terms["wiley"])

        strb.write("\\textbf{Total} &   &  0 & 0\\\\ \n")
        strb.write("\hline\n")
        strb.write("\end{tabular}\n")
        strb.write("\caption{Search execution results for each Search Location}")
        strb.write("\\vspace{-0.4cm}\n")
        strb.write("\end{table}\n")
        strb.write("% ---------------------------\n")
        strb.write("% Search terms table code END\n")
        strb.write("% ---------------------------\n")
        return strb.getvalue()