import ROOT
import array


file_linesruna2018_templ = open("Test_Template/dx_1_Templateruna2018.txt")
file_linesrunb2018_templ = open("Test_Template/dx_1_Templaterunb2018.txt")
file_linesrund2018_templ = open("Test_Template/dx_1_Templaterund2018.txt")
# file_linesrunb2017_templ = open("Test_Template/dx_1_Templaterunb2017.txt")
file_linesrunc2017_templ = open("Test_Template/dx_1_Templaterunc2017.txt")
file_linesrund2017_templ = open("Test_Template/dx_1_Templaterund2017.txt")
# file_linesrune2017_templ = open("Test_Template/dx_1_Templaterune2017.txt")

file_linesruna2018_gener = open("Test_Generic/dx_1_Genericruna2018.txt")
file_linesrunb2018_gener = open("Test_Generic/dx_1_Genericrunb2018.txt")
file_linesrund2018_gener = open("Test_Generic/dx_1_Genericrund2018.txt")
# file_linesrunb2017_gener = open("Test_Generic/dx_1_Templaterunb2017.txt")
file_linesrunc2017_gener = open("Test_Generic/dx_1_Genericrunc2017.txt")
file_linesrund2017_gener = open("Test_Generic/dx_1_Genericrund2017.txt")
# file_linesrune2017_gener = open("Test_Generic/dx_1_Templaterune2017.txt")


linesruna2018_templ = file_linesruna2018_templ.readlines()
linesrunb2018_templ = file_linesrunb2018_templ.readlines()
linesrund2018_templ = file_linesrund2018_templ.readlines()
# linesrunb2017_templ = file_linesrunb2017_templ.readlines()
linesrunc2017_templ = file_linesrunc2017_templ.readlines()
linesrund2017_templ = file_linesrund2017_templ.readlines()
# linesrune2017_templ = file_linesrune2017_templ.readlines()

linesruna2018_gener = file_linesruna2018_gener.readlines()
linesrunb2018_gener = file_linesrunb2018_gener.readlines()
linesrund2018_gener = file_linesrund2018_gener.readlines()
# linesrunb2017_gener = file_linesrunb2017_gener.readlines()
linesrunc2017_gener = file_linesrunc2017_gener.readlines()
linesrund2017_gener = file_linesrund2017_gener.readlines()
# linesrune2017_gener = file_linesrune2017_gener.readlines()

lines_templ = linesrunc2017_templ
for l in linesrund2017_templ:
    lines_templ.append(l)
for l in linesruna2018_templ:
    lines_templ.append(l)
for l in linesrunb2018_templ:
    lines_templ.append(l)
for l in linesrund2018_templ:
    lines_templ.append(l)

lines_gener = linesrunc2017_gener
for l in linesrund2017_gener:
    lines_gener.append(l)
for l in linesruna2018_gener:
    lines_gener.append(l)
for l in linesrunb2018_gener:
    lines_gener.append(l)
for l in linesrund2018_gener:
    lines_gener.append(l)


runs_templ = []
sigmas_templ = []
dsigmas_templ = []
for l in lines_templ:
    runs_templ.append(int(l.split('\t')[0]))
    sigmas_templ.append(float(l.split('\t')[1]))
    dsigmas_templ.append(float(l.split('\t')[2]))

arr_runs_templ = array.array('d', runs)
arr_sigmas_templ = array.array('d', sigmas)
arr_dsigmas_templ = array.array('d', dsigmas)

tgr_templ = ROOT.TGraph(len(arr_runs), arr_runs, arr_sigmas)
print arr_runs

tgr_templ.Draw("AP")

tgr_templ.SaveAs("templ_hist.pdf")


