from historic_plots_drawer import *
import run_to_lumi_out_2017
import run_to_lumi_out_2018
# import argparse

def main():
    modules_arr_run_to_lumi = [run_to_lumi_out_2017, run_to_lumi_out_2018]
    lumi_map = {
        '2017': [0,30],
        '2018': [0,70],
    }
    sigma_map = {
        '2017': {'dx':{1:[10,60],2:[5,30],3:[5,30],4:[10,50]},'dz':{1:[40,100],2:[20,60],3:[10,40],4:[30,80]}},
        '2018': {'dx':{1:[10,60],2:[5,30],3:[5,30],4:[10,50]},'dz':{1:[40,100],2:[20,60],3:[10,40],4:[30,80]}}
    }
    for year in ['2017','2018']:
        for direction in ['dx','dz']:
            for layer in range(1,5):
                myDrawer = Drawer(modules_arr_run_to_lumi)
                # myDrawer._create_run_to_lumi_data()
                file_names_gener = []
                file_names_templ = []
                if year == '2017':
                    file_names_gener = [
                        "../../Test_Generic/%s_%s_Genericrunb%s.txt"%(direction,layer,year),
                        "../../Test_Generic/%s_%s_Genericrunc%s.txt"%(direction,layer,year),
                        "../../Test_Generic/%s_%s_Genericrund%s.txt"%(direction,layer,year),
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        # "../../Test_Generic/dx_2_Genericruna2018.txt",
                        # "../../Test_Generic/dx_2_Genericrunb2018.txt",
                        # "../../Test_Generic/dx_2_Genericrund2018.txt",
                    ]
                    file_names_templ = [
                        "../../Test_Template/%s_%s_Templaterunb%s.txt"%(direction,layer,year),
                        "../../Test_Template/%s_%s_Templaterunc%s.txt"%(direction,layer,year),
                        "../../Test_Template/%s_%s_Templaterund%s.txt"%(direction,layer,year),
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        # "../../Test_Generic/dx_2_Genericruna2018.txt",
                        # "../../Test_Generic/dx_2_Genericrunb2018.txt",
                        # "../../Test_Generic/dx_2_Genericrund2018.txt",
                    ]
                elif year == '2018':
                    file_names_gener = [
                        # "../../Test_Generic/dx_2_Genericrunb%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrunc%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrund%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        "../../Test_Generic/%s_%s_Genericruna%s.txt"%(direction,layer,year),
                        "../../Test_Generic/%s_%s_Genericrunb%s.txt"%(direction,layer,year),
                        "../../Test_Generic/%s_%s_Genericrund%s.txt"%(direction,layer,year),
                    ]
                    file_names_templ = [
                        # "../../Test_Template/dx_2_Templaterunb%s.txt"%year,
                        # "../../Test_Template/dx_2_Templaterunc%s.txt"%year,
                        # "../../Test_Template/dx_2_Templaterund%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        "../../Test_Template/%s_%s_Templateruna%s.txt"%(direction,layer,year),
                        "../../Test_Template/%s_%s_Templaterunb%s.txt"%(direction,layer,year),
                        "../../Test_Template/%s_%s_Templaterund%s.txt"%(direction,layer,year),
                    ]
                sigma_vs_lumi_templ = myDrawer.read_data(file_names_templ)
                # print sigma_vs_lumi_templ_2017
                sigma_vs_lumi_templ = myDrawer.convert_sigma_vs_run_to_lumi(
                    sigma_vs_lumi_templ)
                options = "point.sigma_error < 1e-3 or point.sigma_error >= 0.2*point.sigma or point.sigma_error > 1 or math.isnan(point.sigma_error) or math.isnan(point.sigma) or point.sigma < 8"
                sigma_vs_lumi_templ = myDrawer.clean_history_plot(sigma_vs_lumi_templ, options)
                # print(sigma_vs_lumi_templ)
                sigma_vs_lumi_gener = myDrawer.read_data(file_names_gener)
                sigma_vs_lumi_gener = myDrawer.convert_sigma_vs_run_to_lumi(
                    sigma_vs_lumi_gener)
                sigma_vs_lumi_gener = myDrawer.clean_history_plot(sigma_vs_lumi_gener, options)
                out_file_name = "history_plots/history_%s_%s_%s.pdf"%(year, direction, layer)
                # out_file_name = "../../history_plots/history_%s_%s_%s.pdf" % (
                    # year, direction, layer)
                layer_direction = "Barrel Pixel Layer %s, %s direction"%(layer, direction)
                layer_direction = layer_direction.replace("dx", "x")
                layer_direction = layer_direction.replace("dz", "z")
                myDrawer.draw_history_plot(sigma_vs_lumi_templ, sigma_vs_lumi_gener, out_file_name, layer_direction,lumi_map[year][0], lumi_map[year][1], sigma_map[year][direction][layer][0], sigma_map[year][direction][layer][1])

main()
