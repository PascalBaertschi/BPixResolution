from historic_plots_drawer import *
import run_to_lumi_out_2017
import run_to_lumi_out_2018
# import argparse

def shift_lumi(lumi0, val_vs_lumi):
    lumi_arr = array('d',[l.Lumi for l in val_vs_lumi])
    shift_f = lambda x: x+lumi0
    lumi_arr = map(shift_f, lumi_arr)
    val_arr = array('d',[l.sigma for l in val_vs_lumi])
    val_err_arr = array('d',[l.sigma_error for l in val_vs_lumi])
    dataPoint = namedtuple('dataPoint', 'Lumi, sigma, sigma_error')
    list_points = list()
    for i,lumi in enumerate(lumi_arr):
        list_points.append(dataPoint(Lumi=lumi, sigma=val_arr[i], sigma_error=val_err_arr[i]))
    return sorted(list_points, key=attrgetter('Lumi'))

def main():
    modules_arr_run_to_lumi = [run_to_lumi_out_2017, run_to_lumi_out_2018]
    lumi_shift = {
        '2017': 0,
        '2018': 51.7,
    }
    lumi_map = {
        '2017': [0,51.7],
        '2018': [51.7,120],
    }
    lumi_map_years = {
        '2017_2018': [0,120],
    }
    val_map = {
        'sigma':{
            '2017': {'x':{1:[10,60],2:[5,30],3:[5,30],4:[10,50]},'z':{1:[40,100],2:[20,60],3:[10,40],4:[30,80]}},
            '2018': {'x':{1:[10,60],2:[5,30],3:[5,30],4:[10,50]},'z':{1:[40,100],2:[20,60],3:[10,40],4:[30,80]}}
        },
        'mu':{
            '2017': {'x':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]},'z':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]}},
            '2018': {'x':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]},'z':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]}}
        },
    }
    val_map_years = {
        'sigma':{
            '2017_2018': {'x':{1:[10,60],2:[5,30],3:[5,30],4:[10,50]},'z':{1:[40,100],2:[20,60],3:[10,40],4:[30,80]}},
            # '2018': {'x':{1:[10,60],2:[5,30],3:[5,30],4:[10,50]},'z':{1:[40,100],2:[20,60],3:[10,40],4:[30,80]}}
        },
        'mu':{
            '2017_2018': {'x':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]},'z':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]}},
            # '2018': {'x':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]},'z':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]}}
        },
    }
    # val_map_years = {
    #     'sigma':{
    #         '2017_2018': {'x':{1:[5,60],2:[5,60],3:[5,60],4:[5,60]},'z':{1:[10,100],2:[10,100],3:[10,100],4:[10,100]}},
    #         # '2018': {'x':{1:[10,60],2:[5,30],3:[5,30],4:[10,50]},'z':{1:[40,100],2:[20,60],3:[10,40],4:[30,80]}}
    #     },
    #     'mu':{
    #         '2017_2018': {'x':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]},'z':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]}},
    #         # '2018': {'x':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]},'z':{1:[-20,20],2:[-20,20],3:[-20,20],4:[-20,20]}}
    #     },
    # }
    plot_all_years = True
    sigma_vs_lumi_templ_clean_all_years = list()
    mu_vs_lumi_templ_clean_all_years = list()
    sigma_vs_lumi_gener_clean_all_years = list()
    mu_vs_lumi_gener_clean_all_years = list()

    sigma_vs_lumi_templ_clean_all_years_vs_run = list()
    mu_vs_lumi_templ_clean_all_years_vs_run = list()
    sigma_vs_lumi_gener_clean_all_years_vs_run = list()
    mu_vs_lumi_gener_clean_all_years_vs_run = list()
    parent_dir = "history_plot_templ_changes"
    for direction in ['x','z']:
        for layer in range(1,5):
            for year in ['2017','2018']:
                myDrawer = Drawer(modules_arr_run_to_lumi)
                # myDrawer._create_run_to_lumi_data()
                file_names_sigma_gener = []
                file_names_sigma_templ = []
                if year == '2017':
                    file_names_sigma_gener = [
                        "../../historic_plots/Generic/d%s_%s_Genericrunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/d%s_%s_Genericrunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/d%s_%s_Genericrund%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/d%s_%s_Genericrune%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/d%s_%s_Genericrunf%s.txt"%(direction,layer,year),
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        # "../../Test_Generic/dx_2_Genericruna2018.txt",
                        # "../../Test_Generic/dx_2_Genericrunb2018.txt",
                        # "../../Test_Generic/dx_2_Genericrund2018.txt",
                    ]
                    file_names_sigma_templ = [
                        "../../historic_plots/Template/d%s_%s_Templaterunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/d%s_%s_Templaterunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/d%s_%s_Templaterund%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/d%s_%s_Templaterune%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/d%s_%s_Templaterunf%s.txt"%(direction,layer,year),
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        # "../../Test_Generic/dx_2_Genericruna2018.txt",
                        # "../../Test_Generic/dx_2_Genericrunb2018.txt",
                        # "../../Test_Generic/dx_2_Genericrund2018.txt",
                    ]
                elif year == '2018':
                    file_names_sigma_gener = [
                        # "../../Test_Generic/dx_2_Genericrunb%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrunc%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrund%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        "../../historic_plots/Generic/d%s_%s_Genericruna%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/d%s_%s_Genericrunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/d%s_%s_Genericrunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/d%s_%s_Genericrund%s.txt"%(direction,layer,year),
                    ]
                    file_names_sigma_templ = [
                        # "../../Test_Template/dx_2_Templaterunb%s.txt"%year,
                        # "../../Test_Template/dx_2_Templaterunc%s.txt"%year,
                        # "../../Test_Template/dx_2_Templaterund%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        "../../historic_plots/Template/d%s_%s_Templateruna%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/d%s_%s_Templaterunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/d%s_%s_Templaterunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/d%s_%s_Templaterund%s.txt"%(direction,layer,year),
                    ]
                file_names_mu_gener = []
                file_names_mu_templ = []
                if year == '2017':
                    file_names_mu_gener = [
                        "../../historic_plots/Generic/%s_%s_Genericrunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/%s_%s_Genericrunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/%s_%s_Genericrund%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/%s_%s_Genericrune%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/%s_%s_Genericrunf%s.txt"%(direction,layer,year),
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        # "../../Test_Generic/dx_2_Genericruna2018.txt",
                        # "../../Test_Generic/dx_2_Genericrunb2018.txt",
                        # "../../Test_Generic/dx_2_Genericrund2018.txt",
                    ]
                    file_names_mu_templ = [
                        "../../historic_plots/Template/%s_%s_Templaterunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/%s_%s_Templaterunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/%s_%s_Templaterund%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/%s_%s_Templaterune%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/%s_%s_Templaterunf%s.txt"%(direction,layer,year),
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        # "../../Test_Generic/dx_2_Genericruna2018.txt",
                        # "../../Test_Generic/dx_2_Genericrunb2018.txt",
                        # "../../Test_Generic/dx_2_Genericrund2018.txt",
                    ]
                elif year == '2018':
                    file_names_mu_gener = [
                        # "../../Test_Generic/dx_2_Genericrunb%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrunc%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrund%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        "../../historic_plots/Generic/%s_%s_Genericruna%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/%s_%s_Genericrunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/%s_%s_Genericrunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Generic/%s_%s_Genericrund%s.txt"%(direction,layer,year),
                    ]
                    file_names_mu_templ = [
                        # "../../Test_Template/dx_2_Templaterunb%s.txt"%year,
                        # "../../Test_Template/dx_2_Templaterunc%s.txt"%year,
                        # "../../Test_Template/dx_2_Templaterund%s.txt"%year,
                        # "../../Test_Generic/dx_2_Genericrune2017.txt",
                        "../../historic_plots/Template/%s_%s_Templateruna%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/%s_%s_Templaterunb%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/%s_%s_Templaterunc%s.txt"%(direction,layer,year),
                        "../../historic_plots/Template/%s_%s_Templaterund%s.txt"%(direction,layer,year),
                    ]
                
                options = "point.sigma_error < 1e-3 or point.sigma_error >= 0.2*point.sigma or point.sigma_error > 1 or math.isnan(point.sigma_error) or math.isnan(point.sigma) or point.sigma < 8"
                
                sigma_vs_lumi_templ = myDrawer.read_data(file_names_sigma_templ)
                sigma_vs_lumi_templ_vs_run = myDrawer.convert_sigma_vs_run(sigma_vs_lumi_templ)
                sigma_vs_lumi_templ = myDrawer.convert_sigma_vs_run_to_lumi(sigma_vs_lumi_templ)
                sigma_vs_lumi_templ_clean = myDrawer.clean_history_plot(sigma_vs_lumi_templ, sigma_vs_lumi_templ, options)
                mu_vs_lumi_templ = myDrawer.read_data(file_names_mu_templ)
                mu_vs_lumi_templ_vs_run = myDrawer.convert_sigma_vs_run(mu_vs_lumi_templ)
                mu_vs_lumi_templ = myDrawer.convert_sigma_vs_run_to_lumi(mu_vs_lumi_templ)
                mu_vs_lumi_templ_clean = myDrawer.clean_history_plot(sigma_vs_lumi_templ, mu_vs_lumi_templ, options)
                sigma_vs_lumi_gener = myDrawer.read_data(file_names_sigma_gener)
                sigma_vs_lumi_gener_vs_run = myDrawer.convert_sigma_vs_run(sigma_vs_lumi_gener)
                sigma_vs_lumi_gener = myDrawer.convert_sigma_vs_run_to_lumi(sigma_vs_lumi_gener)
                sigma_vs_lumi_gener_clean = myDrawer.clean_history_plot(sigma_vs_lumi_gener, sigma_vs_lumi_gener, options)
                mu_vs_lumi_gener = myDrawer.read_data(file_names_mu_gener)
                mu_vs_lumi_gener_vs_run = myDrawer.convert_sigma_vs_run(mu_vs_lumi_gener)
                mu_vs_lumi_gener = myDrawer.convert_sigma_vs_run_to_lumi(mu_vs_lumi_gener)
                mu_vs_lumi_gener_clean = myDrawer.clean_history_plot(sigma_vs_lumi_gener, mu_vs_lumi_gener, options)
                
                sigma_vs_lumi_templ_clean_vs_run = myDrawer.clean_history_plot(sigma_vs_lumi_templ_vs_run, sigma_vs_lumi_templ_vs_run, options)
                mu_vs_lumi_templ_clean_vs_run = myDrawer.clean_history_plot(mu_vs_lumi_templ_vs_run, mu_vs_lumi_templ_vs_run, options)
                sigma_vs_lumi_gener_clean_vs_run = myDrawer.clean_history_plot(sigma_vs_lumi_gener_vs_run, sigma_vs_lumi_gener_vs_run, options)
                mu_vs_lumi_gener_clean_vs_run = myDrawer.clean_history_plot(mu_vs_lumi_gener_vs_run, mu_vs_lumi_gener_vs_run, options)

                sigma_vs_lumi_templ_clean = shift_lumi(lumi_shift[year],sigma_vs_lumi_templ_clean)
                mu_vs_lumi_templ_clean = shift_lumi(lumi_shift[year],mu_vs_lumi_templ_clean)
                sigma_vs_lumi_gener_clean = shift_lumi(lumi_shift[year],sigma_vs_lumi_gener_clean)
                mu_vs_lumi_gener_clean = shift_lumi(lumi_shift[year],mu_vs_lumi_gener_clean)

                direction2 = None
                if 'x' in direction: direction2 = rt.TString('r-#phi')
                else: direction2 = direction
                layer_direction = "Barrel Pixel Layer %s, %s direction"%(layer, direction2)
                
                val = "sigma"
                out_file_name = "%s/history_%s_%s_%s_%s.pdf"%(parent_dir,year, direction, layer, val)
                myDrawer.draw_history_plot(sigma_vs_lumi_templ_clean, sigma_vs_lumi_gener_clean, out_file_name, val,layer_direction,lumi_map[year][0], lumi_map[year][1], val_map[val][year][direction][layer][0], val_map[val][year][direction][layer][1])
                val = "mu"
                out_file_name = "%s/history_%s_%s_%s_%s.pdf"%(parent_dir,year, direction, layer, val)
                myDrawer.draw_history_plot(mu_vs_lumi_templ_clean, mu_vs_lumi_gener_clean, out_file_name, val, layer_direction,lumi_map[year][0], lumi_map[year][1], val_map[val][year][direction][layer][0], val_map[val][year][direction][layer][1])
                if plot_all_years:
                    a = shift_lumi(lumi_shift[year],sigma_vs_lumi_templ_clean)
                    sigma_vs_lumi_templ_clean_all_years.extend(sigma_vs_lumi_templ_clean)
                    mu_vs_lumi_templ_clean_all_years.extend(mu_vs_lumi_templ_clean)
                    sigma_vs_lumi_gener_clean_all_years.extend(sigma_vs_lumi_gener_clean)
                    mu_vs_lumi_gener_clean_all_years.extend(mu_vs_lumi_gener_clean)
                    sigma_vs_lumi_templ_clean_all_years_vs_run.extend(shift_lumi(0,sigma_vs_lumi_templ_clean_vs_run))
                    mu_vs_lumi_templ_clean_all_years_vs_run.extend(shift_lumi(0,mu_vs_lumi_templ_clean_vs_run))
                    sigma_vs_lumi_gener_clean_all_years_vs_run.extend(shift_lumi(0,sigma_vs_lumi_gener_clean_vs_run))
                    mu_vs_lumi_gener_clean_all_years_vs_run.extend(shift_lumi(0,mu_vs_lumi_gener_clean_vs_run))
            
            
            val = "sigma"
            addit = "_templ_"
            years = "2017_2018"
            out_file_name = "%s/history_%s_%s_%s_%s%s.pdf"%(parent_dir,years, direction, layer, val, addit)
            myDrawer.draw_history_plot(sigma_vs_lumi_templ_clean_all_years, sigma_vs_lumi_gener_clean_all_years, out_file_name, val,layer_direction,lumi_map_years[years][0], lumi_map_years[years][1], val_map_years[val][years][direction][layer][0], val_map_years[val][years][direction][layer][1])
            
            out_file_name = "%s/history_vs_run_%s_%s_%s_%s%s.pdf"%(parent_dir,years, direction, layer, val, addit)
            myDrawer.draw_history_plot(sigma_vs_lumi_templ_clean_all_years_vs_run, sigma_vs_lumi_gener_clean_all_years_vs_run, out_file_name, val,layer_direction,294904,327564, val_map_years[val][years][direction][layer][0], val_map_years[val][years][direction][layer][1])
            
            
            val = "mu"
            out_file_name = "%s/history_%s_%s_%s_%s%s.pdf"%(parent_dir,years, direction, layer, val, addit)
            myDrawer.draw_history_plot(mu_vs_lumi_templ_clean_all_years, mu_vs_lumi_gener_clean_all_years, out_file_name, val, layer_direction,lumi_map_years[years][0], lumi_map_years[years][1], val_map_years[val][years][direction][layer][0], val_map_years[val][years][direction][layer][1])
            
            out_file_name = "%s/history_vs_run_%s_%s_%s_%s%s.pdf"%(parent_dir,years, direction, layer, val, addit)
            # myDrawer.draw_history_plot(mu_vs_lumi_templ_clean_all_years_vs_run, mu_vs_lumi_gener_clean_all_years_vs_run, out_file_name, val, layer_direction,lumi_map_years[years][0], lumi_map_years[years][1], val_map_years[val][years][direction][layer][0], val_map_years[val][years][direction][layer][1])
            
            
            sigma_vs_lumi_templ_clean_all_years = list()
            mu_vs_lumi_templ_clean_all_years = list()
            sigma_vs_lumi_gener_clean_all_years = list()
            mu_vs_lumi_gener_clean_all_years = list()

            sigma_vs_lumi_templ_clean_all_years_vs_run = list()
            mu_vs_lumi_templ_clean_all_years_vs_run = list()
            sigma_vs_lumi_gener_clean_all_years_vs_run = list()
            mu_vs_lumi_gener_clean_all_years_vs_run = list()

main()