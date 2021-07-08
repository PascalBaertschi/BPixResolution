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

    def _intlumi_to_run(self, lumi):
        run = None
        for r, l in self.run_to_lumi_data.items():
            if l == lumi:
                run = float(r)
        return run
    
    def convert_sigma_vs_run_to_lumi(self, sigma_vs_run):
        list_points = list()
        dataPoint = namedtuple('dataPoint', 'Lumi, sigma, sigma_error')
        for run in sigma_vs_run:
            list_points.append(dataPoint(Lumi=self._run_to_intlumi(run), sigma=sigma_vs_run[run][0], sigma_error=sigma_vs_run[run][1]))
        return sorted(list_points, key=attrgetter('Lumi'))

    def convert_sigma_vs_run(self, sigma_vs_run):
        list_points = list()
        dataPoint = namedtuple('dataPoint', 'Lumi, sigma, sigma_error')
        for run in sigma_vs_run:
            list_points.append(dataPoint(Lumi=run, sigma=sigma_vs_run[run][0], sigma_error=sigma_vs_run[run][1]))
        return sorted(list_points, key=attrgetter('Lumi'))
    
    def clean_history_plot(self, list_points, list_points_to_clean, options = None):
        new_list_points = list()
        bool_opt = None
        for i,point in enumerate(list_points):
            # print("%s - %s"%(point.Lumi, list_points_to_clean[i].Lumi))
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
            
    def draw_history_plot(self, val_vs_lumi_templ, val_vs_lumi_gener, out_file_name, val, layer_direction, lint_min=0., lint_max=100., sigma_min=0., sigma_max=100.):
        a = [l.Lumi for l in val_vs_lumi_templ]
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
        tl0 = rt.TLine(0,sigma_min,0,sigma_max)
        tl = rt.TLine(51.7,sigma_min,51.7,sigma_max)
        tl0.SetLineWidth(2)
        tl.SetLineWidth(2)
        # tl.SetLineStyle(1)
        tl.SetLineColor(rt.kBlack)
        tl0.SetLineColor(rt.kBlack)
        tl_gain_calib = list()
        tl_iovs = list()
        tl_hv_change = list()
        run_list_gain_calib =       [298652,303789,312202,318226,319936,319942,320376,323231,326850]
        run_list_gain_calib_corr = [298652,303790,318346,319941,320384,323318,326853]
        run_iovs =      [297280,298652,299442,300388,301045,302130,303789,303997,304910,313040,314880,316757,317526,317660,317663,318226,320376,321830,322509,322602,323231,324244]
        run_iovs_corr = [297280,298652,299442,300386,301046,302131,303790,303997,305040,315257,314878,316757,317527,317661,317663,318346,320384,321831,322510,322602,323318,324245]
        run_iovs_corr = [296641,297179,297215,297280,298652,299442,298998,299443,300386,301046,302131,303790,303997,305040,314889,316757,317488,317527,317661,317663,317683,318346,319950,320384,320500,321831,322510,322602,322617,323318,324245]
        # run_iovs_corr = [296641, 297179, 297215,298998,299443]314883,317488,317682,319948,320494,322619
        runs_hv_change = [297281,300389,302131,318622,323376]
        run_hv_change_corr = runs_hv_change[:]

        # run_clean = True
        # run_gc = True and not run_clean
        # run_tc = not run_gc and not run_clean

        run_clean = False
        run_gc = False
        run_tc = True
        hvs = [11.8, 19.9, 20.3, 20.7, 51.8, 74.8, 75.2, 75.6, 106.8]
        cols = [618,  633,  601,  434,  633,  618,  601,  434,  633]
        gains = [6.4, 24.8, 52.1, 75.5, 80.9, 83.1, 107.0, 119.5]
        # for lg in gains:
        #     lumi = lg
        #     tl_gain_calib.append(rt.TLine(lumi,sigma_min,lumi,sigma_max))
        #     # print "%s - %s"%(run_calib, self.run_to_lumi_data[run_calib])
        # for i,lhv in enumerate(hvs):
        #     lumi = lhv
        #     tl_iovs.append(rt.TLine(lumi,sigma_min,lumi,sigma_max))
        #     tl_iovs[i].SetLineColor(cols[i])
        for run_calib in run_list_gain_calib_corr:
            lumi = self.run_to_lumi_data[run_calib]
            if run_calib > 313000:
                lumi += 50
            tl_gain_calib.append(rt.TLine(lumi,sigma_min,lumi,sigma_max))
            # print "%s - %s"%(run_calib, self.run_to_lumi_data[run_calib])
        for run_iov in run_iovs_corr:
            lumi = self.run_to_lumi_data[run_iov]
            if run_iov > 313000:
                lumi += 51.7
            tl_iovs.append(rt.TLine(lumi,sigma_min,lumi,sigma_max))
        for run_hv in run_hv_change_corr:
            lumi = self.run_to_lumi_data[run_hv]
            if run_hv > 313000:
                lumi += 51.7
            tl_hv_change.append(rt.TLine(lumi,sigma_min,lumi,sigma_max))
                # print "%s- %s"%(run_iov, lumi)
        # 290543 - 298652: Contains SiPixelGainCalibration_2017_v2_bugfix / SiPixelGainCalibration_hlt_2017_v2_bugfix (Pre-TS1)
        # 298653 - 303789: Contains SiPixelGainCalibration_2017_v5 / SiPixelGainCalibration_2017_hlt_v5 (TS1-TS2)
        # 303790 - 312202: Contains SiPixelGainCalibration_2017_v6 / SiPixelGainCalibration_2017_hlt_v6 (Post-TS2)
        # 312203 - 318226: Contains SiPixelGainCalibration_2018_v2_fine / SiPixelGainCalibration_2018_hlt_v2_fine (PreMD1 in 2018) //PH132
        # 318227 - 319936: Contains SiPixelGainCalibration_2018_v4_fine / SiPixelGainCalibration_2018_hlt_v4_fine (PostMD1 - PreMD2 in 2018) //PH132
        # 319937 - 319942: Contains SiPixelGainCalibration_2018_v5 / SiPixelGainCalibration_hlt_2018_v5 //special fill before MD2 w/ PH142
        # 319943 - 320376: Contains SiPixelGainCalibration_2018_v4_fine / SiPixelGainCalibration_2018_hlt_v4_fine (PostMD1 - PreMD2 in 2018) //PH132
        # 320377 - 323231: Contains SiPixelGainCalibration_2018_v6 / SiPixelGainCalibration_hlt_2018_v6 (postMD2) // PH142
        # 323232 - 326850: Contains SiPixelGainCalibration_2018_v7 / SiPixelGainCalibration_hlt_2018_v7_bugfix (post MD3/TS2)
        # 326851 - infinity: Contains SiPixelGainCalibration_2018_v9 / SiPixelGainCalibration_hlt_2018_v9 (post-TS3)
        # 290543 - 297280: Contains *_phase1_38T_2017_rereco_v1
        # 297281 - 298652: Contains *_phase1_38T_2017_rereco_v2
        # 298653 - 299442: Contains *_phase1_38T_2017_rereco_v3
        # 299443 - 300388: Contains *_phase1_38T_2017_ultralegacy_v8
        # 300389 - 301045: Contains *_phase1_38T_2017_ultralegacy_v9
        # 301046 - 302130: Contains *_phase1_38T_2017_ultralegacy_v10
        # 302131 - 303789: Contains *_phase1_38T_2017_ultralegacy_v11
        # 303790 - 303997: Contains S*_phase1_38T_2017_ultralegacy_v12
        # 303998 - 304910: Contains *_phase1_38T_2017_ultralegacy_v13_bugfix
        # 304911 - 313040: Contains *_phase1_38T_2017_ultralegacy_v14
        # 313041 - 314880: Contains *_phase1_38T_2018_rereco_v1 (CRAFT starts here)
        # 314881 - 316757: Contains *_phase1_38T_2018_rereco_v2 (L1@400V)
        # 316758 - 317526: Contains *_phase1_38T_2018_rereco_v3 (change due to irradiation)
        # 317527 - 317660: Contains *_phase1_38T_2018_rereco_v4 (change due to irradiation)
        # 317661 - 317663: Contains *_phase1_38T_2018_rereco_v5BasedOnGainV2 (post-TS1 settings)
        # 317664 - 318226: Contains *_phase1_38T_2018_rereco_v4 (change due to irradiation)
        # 318227 - 320376: Contains *_phase1_38T_2018_rereco_v5BasedOnGainV2 (post-TS1)
        # 320377 - 321830: Contains *_phase1_38T_2018_v8 (post-MD2)
        # 321831 - 322509: Contains *_phase1_38T_2018_v9 // change due to irradiation
        # 322510 - 322602: Contains *_phase1_38T_2018_v10 // test HV fill for alignment derivation purpose
        # 322603 - 323231: Contains *_phase1_38T_2018_v9 // back to the normal conditions that time
        # 323232 - 324244: Contains *_phase1_38T_2018_ultralegacy_v9 // then we realized that FPix HV has to be changed too, so v10 is not good, post-TS2 conditions, redone for UL
        # 324245 - inf: Contains *_phase1_38T_2018_ultralegacy_v10 // Era-F boundary, redone for UL
        canva = rt.TCanvas("c1","c1",0,0,2500,1000)
        empty_hist = rt.TH1D("History plot", "", n_empty, lint_min, lint_max)
        empty_hist.GetYaxis().SetRangeUser(sigma_min,sigma_max)
        empty_hist.GetXaxis().SetTitle("Delivered Luminosity - Phase-1 [fb^{-1}]")
        if "mu" in val: empty_hist.GetYaxis().SetTitle("#%s, #mum"%val)
        else:
            layer_direction_new = layer_direction.replace('r-#phi','r-  #phi')
            empty_hist.GetYaxis().SetTitle("%s resolution, %s [#mum]"%(layer_direction_new.split(',')[0],layer_direction_new.split(',')[1]))
        # if "sigma" in val:
        #     if 'r-#phi' in layer_direction.split(',')[1]:
        #         empty_hist.GetYaxis().SetTitle("Pixel resolution r- #phi direction [#mum]")
        #     else:
        #         empty_hist.GetYaxis().SetTitle("Pixel resolution z direction [#mum]")
        rt.gStyle.SetOptStat(000000)
        leg = rt.TLegend(0.7, 0.68, 0.89, 0.89)
        n_templ = len(lumi_arr_templ)
        n_gener = len(lumi_arr_gener)
        tgr_templ = rt.TGraphErrors(n_templ, lumi_arr_templ, val_templ_arr, array('d',[0]*n_templ), val_templ_err_arr)
        tgr_gener = rt.TGraphErrors(n_gener, lumi_arr_gener, val_gener_arr, array('d',[0]*n_gener), val_gener_err_arr)
        leg.AddEntry(tl, "First run of a year", "l")
        leg.AddEntry(tl_hv_change[0], "Pixel HV change", "l")
        leg.AddEntry(tl_iovs[0], "Pixel calibration change", "l")
        leg.AddEntry(tl_gain_calib[0], "Pixel gain change", "l")
        leg.AddEntry(tgr_templ, "Template reconstruction", "pl")
        leg.AddEntry(tgr_gener, "Generic reconstruction", "pl")
        options_gener = """SetMarkerStyle(21),SetMarkerColor(rt.kRed),SetLineColor(rt.kRed),SetLineWidth(2),SetMarkerSize(0.7)"""
        options_templ = """SetMarkerStyle(20),SetMarkerColor(rt.kBlue),SetLineColor(rt.kBlue),SetLineWidth(2),SetMarkerSize(0.7)"""
        self._style_graph(tgr_templ, options_templ)
        self._style_graph(tgr_gener, options_gener)
        empty_hist.Draw()
        tl0.Draw("same l")
        if lint_max > 60 or lint_min<50.: tl.Draw("same l")
        for t in tl_iovs:
            t.SetLineStyle(2)
            t.SetLineColor(rt.kGray+2)
            t.Draw("same l")
        for t in tl_gain_calib:
            t.SetLineStyle(3)
            t.SetLineColor(rt.kGray+2)
            t.Draw("same l")
        for t in tl_hv_change:
            t.SetLineStyle(7)
            t.Draw("same l")
        tgr_templ.Draw("same p")
        tgr_gener.Draw("same p")
        t = canva.GetTopMargin()
        b = canva.GetBottomMargin()
        r = canva.GetRightMargin()
        l = canva.GetLeftMargin()
        leg1 = rt.TLegend(0.1,0.82,0.13+0.003,0.855)
        leg1.Draw()
        leg2 = rt.TLegend((1-l-r)/120.*51.7+l,0.8,(1-l-r)/120.*51.7+l+0.03+0.003,0.835)
        leg2.Draw()
        leg3 = rt.TLegend(0.2,0.72,0.28,0.78)
        leg3.SetBorderSize(0)
        leg3.Draw()
        self._cms_draw(canva, layer_direction)
        # tl_iovs[0].SetLineColor(rt.kBlack)
        leg.Draw("same")
        canva.SaveAs(out_file_name)

    def _cms_draw(self, canvas, layer_direction):
        cmsText = "CMS"
        cmsTextFont = 61
        writeExtraText = True
        # extraText = "Work in progress"
        extraText = "Preliminary"
        # extraText2 = "(2017+2018 pp collisions)"
        # extraText2 = '119.5 fb^\{-1\} (2017+2018, 13 TeV)'
        extraText3 = "CMS FLUKA study v3.23.1.0"
        cmsextratext = '#bf{CMS} #it{Preliminary} (2017+2018 pp collisions)'
        extraTextFont = 51
        lumiTextSize = 0.5
        lumiTextOffset = 0.0
        cmsTextSize = 0.5
        cmsTextOffset = 0.1
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
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11)
        latex.SetTextSize(cmsTextSize*t)
        latex.DrawLatex(l+0.01, 1-t+0.01, cmsText)
        latex.SetTextFont(extraTextFont)
        latex.SetTextSize(extraTextSize*t)
        latex.DrawLatex(l+0.01+0.045, 1-t+0.01, extraText)
        latex.SetTextFont(extraTextFont-10)
        latex.SetTextFont(51)
        latex.SetTextSize(extraTextSize*t*0.85)
        latex.SetTextSize(extraTextSize*t*1.2)
        latex.SetTextFont(42)
        latex.SetTextSize(extraTextSize*t)
        latex.DrawLatex(0.2+0.002,0.72+0.018, '#bf{p_{T} > 12 GeV}')
        latex.DrawLatex(1-r-0.145-0.035, 1-t+0.01, '119.5 fb^{-1} (2017+2018, 13 TeV)')
        latex.DrawLatex(0.1+0.001,0.82+0.004, '#bf{2017}')
        latex.DrawLatex((1-l-r)/120.*51.7+l+0.001,0.8+0.004, '#bf{2018}')