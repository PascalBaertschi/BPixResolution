# BPixResolution plot

Create folders with names file_nice_plots, file_nice_plots/Template, file_nice_plots/Generic.

The plotting code for BPix Residual Triplets studies.

The main plotting code: run_new_layer4_in_out.C

Run:
`root -l run_new_layer4_in_out.C\(\"Name_of_the_input_file.root\",\"Reco\"\) -b -q`
Reco is Template or Generic.

The plots are created in file_nice_plots/Template and file_nice_plots/Generic.

# History plots

Create folders with names historic_plots, historic_plots/Test_Template, historic_plots/Test_Generic.

Run:
`root -l FitAndPlot_tree_bpix_new.C\(\"run_year\",\"Reco\"\) -b -q`
run_year is of the following structure `path/to/file/run{epoch}{year}`, for example `files_lists/runa2018` (without extension). 

The example of the file list:
```
...
root://t3se01.psi.ch:1094//store/user/dbrzhech/Pxl_res/HistoryPlots/SingleMuon/RunALCARECOHistory-2018A-110X_dataRun2_v12/200811_010321/0000/Resolution_123.root
root://t3se01.psi.ch:1094//store/user/dbrzhech/Pxl_res/HistoryPlots/SingleMuon/RunALCARECOHistory-2018A-110X_dataRun2_v12/200811_010321/0000/Resolution_124.root
root://t3se01.psi.ch:1094//store/user/dbrzhech/Pxl_res/HistoryPlots/SingleMuon/RunALCARECOHistory-2018A-110X_dataRun2_v12/200811_010321/0000/Resolution_125.root
root://t3se01.psi.ch:1094//store/user/dbrzhech/Pxl_res/HistoryPlots/SingleMuon/RunALCARECOHistory-2018A-110X_dataRun2_v12/200811_010321/0000/Resolution_126.root
root://t3se01.psi.ch:1094//store/user/dbrzhech/Pxl_res/HistoryPlots/SingleMuon/RunALCARECOHistory-2018A-110X_dataRun2_v12/200811_010321/0000/Resolution_127.root
root://t3se01.psi.ch:1094//store/user/dbrzhech/Pxl_res/HistoryPlots/SingleMuon/RunALCARECOHistory-2018A-110X_dataRun2_v12/200811_010321/0000/Resolution_128.root
...
```

After this, you should find all of the plots created in historic_plots/Template, historic_plots/Generic folders. Also, there will be .txt with the following names: `d{direction}_{layer}_{reco}run{epoch}{year}.txt` with run vs sigma and sigma error and `{direction}_{layer}_{reco}run{epoch}{year}.txt`.

To produce historic plots run `python history_plot_creator.py -b`.