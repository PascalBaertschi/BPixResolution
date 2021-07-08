# root -l FitAndPlot_tree_bpix_new.C\(\"runb2017\",\"Template\"\) -b -q >> log_2017b_mean_templ.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"runc2017\",\"Template\"\) -b -q >> log_2017c_mean_templ.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"rund2017\",\"Template\"\) -b -q >> log_2017d_mean_templ.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"rund2018\",\"Template\"\) -b -q >> log_2018d_mean_templ.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"runb2018\",\"Template\"\) -b -q >> log_2018b_mean_templ.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"runa2018\",\"Template\"\) -b -q >> log_2018a_mean_templ.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"runb2017\",\"Generic\"\) -b -q >> log_2017b_mean_gen.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"runc2017\",\"Generic\"\) -b -q >> log_2017c_mean_gen.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"rund2017\",\"Generic\"\) -b -q >> log_2017d_mean_gen.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"rund2018\",\"Generic\"\) -b -q >> log_2018d_mean_gen.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"runb2018\",\"Generic\"\) -b -q >> log_2018b_mean_gen.txt &
# root -l FitAndPlot_tree_bpix_new.C\(\"runa2018\",\"Generic\"\) -b -q >> log_2018a_mean_gen.txt &
cd /afs/cern.ch/user/d/dbrzhech/ServiceWork/BPixResolution/CMSSW_11_1_0_pre1/src/DPGAnalysis-SiPixelTools/PixelTriplets
root -l BPixResolution/BPixResolution/FitAndPlot_tree_bpix_new.C\(\"rune2017\",\"Template\"\) -b -q > log_rune2017_Template.log &
root -l BPixResolution/BPixResolution/FitAndPlot_tree_bpix_new.C\(\"rune2017\",\"Generic\"\) -b -q > log_rune2017_Generic.log &
root -l BPixResolution/BPixResolution/FitAndPlot_tree_bpix_new.C\(\"runf2017\",\"Template\"\) -b -q > log_runf2017_Template.log &
root -l BPixResolution/BPixResolution/FitAndPlot_tree_bpix_new.C\(\"runf2017\",\"Generic\"\) -b -q > log_runf2017_Generic.log &
root -l BPixResolution/BPixResolution/FitAndPlot_tree_bpix_new.C\(\"runc2018\",\"Template\"\) -b -q > log_runc2018_Template.log &
root -l BPixResolution/BPixResolution/FitAndPlot_tree_bpix_new.C\(\"runc2018\",\"Generic\"\) -b -q > log_runc2018_Generic.log &
