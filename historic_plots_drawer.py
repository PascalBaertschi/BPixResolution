import ROOT as rt
from array import array
from collections import namedtuple
from operator import attrgetter
import math

class Drawer(object):
    
    def __init__(self, modules_array):
        self.run_to_lumi_data = self._create_run_to_lumi_data(modules_array)
    
    def _create_run_to_lumi_data(self, modules_array):
        run_to_lumi_data = dict()
        # self.modules_array = list()
        self.modules_array = modules_array
        for i,module_name in enumerate(modules_array):
            # self.modules_array.append(importlib.import_module(module_name))
            run_to_lumi_data.update(self.modules_array[i].run_to_lumi)
        return run_to_lumi_data

    def _read_data_file(self, input_file_name):
        input_file = open(input_file_name, "r")
        lines = input_file.readlines()
        lines = [l.split('\t') for l in lines]
        runs = [int(l[0]) for i,l in enumerate(lines)]
        # print runs
        sigmas = [float(l[1]) for i,l in enumerate(lines)]
        # print sigmas
        sigmas_errs = [float(l[2]) for i,l in enumerate(lines)]
        # print sigmas_errs
        sigma_vs_run = dict()
        for i,r in enumerate(runs):
            sigma_vs_run[r] = [sigmas[i], sigmas_errs[i]]
        input_file.close()
        return sigma_vs_run #self
    
    def read_data(self, file_names):
        sigma_vs_run_full = dict()
        for f in file_names:
            s_vs_r = self._read_data_file(f)
            sigma_vs_run_full.update(s_vs_r)
        return sigma_vs_run_full #self

    def _run_to_intlumi(self, run):
        lumi = self.run_to_lumi_data[run]
        return lumi
    
    def convert_sigma_vs_run_to_lumi(self, sigma_vs_run):
        list_points = list()
        dataPoint = namedtuple('dataPoint', 'Lumi, sigma, sigma_error')
        for run in sigma_vs_run:
            list_points.append(dataPoint(Lumi=self._run_to_intlumi(run), sigma=sigma_vs_run[run][0], sigma_error=sigma_vs_run[run][1]))
        return sorted(list_points, key=attrgetter('Lumi'))
    
    def clean_history_plot(self, list_points, list_points_to_clean, options = None):
        new_list_points = list()
        bool_opt = None
        for i,point in enumerate(list_points):
            print("%s - %s"%(point.Lumi, list_points_to_clean[i].Lumi))
            # print("%s +- %s" % (point.sigma, point.sigma_error))
            # bool_opt = None
            # for opt in options:
                # exec("bool_opt = "+opt)
            # "point.sigma_error < 1e-3", "point.sigma_error >= 0.1*point.sigma",
            # "math.isnan(point.sigma_error)", "math.isnan(point.sigma)", "point.sigma<9.", "point.sigma > 20."
            exec('bool_opt = '+options)
            if bool_opt:
                pass
            else:
                new_list_points.append(list_points_to_clean[i])
        return new_list_points

    def _latex(self):
        pass
    
    def _style_graph(self, graph, options):
        options='{0}'+options
        options=options.replace(',',';{0}')
        exec(options.format("graph."))

    # def _conditions_apply(self, options):
    #     # options = ["1: sigma_error < 1e-3; 2: sigma_error >= sigma; 3: lumi < 100.; cond: 1 or 2 and 3", ...]
    #     new_options = list()
        
    #     for i,opt in enumerate(options):
    #         opt_split = opt.split(';')
    #         new_options.append(dict())
    #         for opt_str in opt_split:
    #             opt_str_split = opt_split.split(':')
    #             new_options[i][opt_str_split[0]] = opt_str_split[1]
            
    def draw_history_plot(self, val_vs_lumi_templ, val_vs_lumi_gener, out_file_name, val, layer_direction, lint_min=0., lint_max=100., sigma_min=0., sigma_ymax=100.):
        lumi_arr_templ = array('d',[l.Lumi for l in val_vs_lumi_templ])
        val_templ_arr = array('d',[l.sigma for l in val_vs_lumi_templ])
        val_templ_err_arr = array('d',[l.sigma_error for l in val_vs_lumi_templ])
        lumi_arr_gener = array('d', [l.Lumi for l in val_vs_lumi_gener])
        val_gener_arr = array('d',[l.sigma for l in val_vs_lumi_gener])
        val_gener_err_arr = array('d',[l.sigma_error for l in val_vs_lumi_gener])
        n_empty=100
        # lmin_empty = 0.
        # lmax_empty = 100.
        # lmin_empty = 300000.
        # lmax_empty = 320000.
        canva = rt.TCanvas("c1","c1",0,0,1000,800)
        empty_hist = rt.TH1D("History plot", "", n_empty, lint_min, lint_max)
        empty_hist.GetYaxis().SetRangeUser(sigma_min,sigma_ymax)
        empty_hist.GetXaxis().SetTitle("L_{int}, fb^{-1}")
        empty_hist.GetYaxis().SetTitle("#%s, #mum"%val)
        rt.gStyle.SetOptStat(000000)
        leg = rt.TLegend(0.7, 0.8, 0.9, 0.9)
        n_templ = len(lumi_arr_templ)
        n_gener = len(lumi_arr_gener)
        tgr_templ = rt.TGraphErrors(n_templ, lumi_arr_templ, val_templ_arr, array('d',[0]*n_templ), val_templ_err_arr)
        tgr_gener = rt.TGraphErrors(n_gener, lumi_arr_gener, val_gener_arr, array('d',[0]*n_gener), val_gener_err_arr)
        leg.AddEntry(tgr_templ, "Template")
        leg.AddEntry(tgr_gener, "Generic")
        options_templ = """SetMarkerStyle(8),SetMarkerColor(rt.kRed),SetLineColor(rt.kRed),SetLineWidth(2),SetMarkerSize(0.7)"""
        options_gener = """SetMarkerStyle(21),SetMarkerColor(rt.kBlue),SetLineColor(rt.kBlue),SetLineWidth(2),SetMarkerSize(0.7)"""
        self._style_graph(tgr_templ, options_templ)
        self._style_graph(tgr_gener, options_gener)
        # self._latex(latex_options)
        empty_hist.Draw()
        tgr_templ.Draw("same p")
        tgr_gener.Draw("same p")
        leg.Draw("same")
        self._cms_draw(canva, layer_direction)
        canva.SaveAs(out_file_name)

    def _cms_draw(self, canvas, layer_direction):
        cmsText = "CMS"
        cmsTextFont = 61
        writeExtraText = True
        extraText = "Work in progress"
        extraText2 = "2020"
        # extraText3 = "CMS FLUKA study v3.23.1.0"
        extraTextFont = 51
        lumiTextSize = 0.5
        lumiTextOffset = 0.0
        cmsTextSize = 0.5
        cmsTextOffset = 0.1
        # only used in outOfFrame version
        relPosX = 0.045
        relPosY = 0.035
        relExtraDY = 1.2
        extraOverCmsTextSize = 0.65
        t = canvas.GetTopMargin()
        b = canvas.GetBottomMargin()
        r = canvas.GetRightMargin()
        l = canvas.GetLeftMargin()
        latex = rt.TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(rt.kBlack)
        extraTextSize = extraOverCmsTextSize*cmsTextSize*1.1
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(lumiTextSize*t)
        # latex.DrawLatex(1-r, 1-t+lumiTextOffset*t, lumiText)
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11)
        latex.SetTextSize(cmsTextSize*t)
        latex.DrawLatex(l, 1-t+0.01, cmsText)
        latex.SetTextFont(extraTextFont)
        latex.SetTextSize(extraTextSize*t)
        # latex.DrawLatex(l+0.05, 1-t+lumiTextOffset*t-0.09-0.06, extraText)
        # latex.DrawLatex(l+0.05+0.06, 1-t+lumiTextOffset*t-0.09, extraText)
        latex.DrawLatex(l+0.12, 1-t+0.01, extraText)
        latex.SetTextFont(extraTextFont-10)
        # latex.DrawLatex(l+0.14, 1-t+lumiTextOffset*t-0.09-0.06, extraText2)
        # latex.DrawLatex(l+0.14+0.06, 1-t+lumiTextOffset*t-0.09, extraText2)
        latex.SetTextFont(51)
        latex.SetTextSize(extraTextSize*t*0.85)
        # latex.DrawLatex(l+0.6, 1-t+lumiTextOffset*t-0.05, extraText3)
        # fpix_logo = "Forward Pixel Ring %s Disk %s" % (self.ring, self.disk)
        # layer_direction = "13 TeV"
        # TrackSelectionText = fpix_logo
        # latex.SetTextFont(61)
        latex.SetTextSize(extraTextSize*t)
        latex.SetTextFont(42)
        latex.DrawLatex(l+0.18, 1-t-0.04, layer_direction)
        latex.DrawLatex(1-l-0.09, 1-t+0.01, "13 TeV")
        # TrackSelctionText2 = ""
        # if self.disk == "1":
        #     TrackSelctionText2 = "z = 32 cm"
        # elif self.disk == "2":
        #     TrackSelctionText2 = "z = 40 cm"
        # elif self.disk == "3":
        #     TrackSelctionText2 = "z = 50 cm"
        # TrackSelctionText2 = "z = 0 cm"
        # TrackSelctionText2 = ""
        # latex.SetTextFont(61)
        # latex.SetTextSize(extraTextSize*t)
        # latex.DrawLatex(l+0.4, 1-t+lumiTextOffset*t -
        #                 0.15-0.04, TrackSelctionText2)