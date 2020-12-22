#include "TH1.h"
#include "TMath.h"
#include "TF1.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TFile.h"
#include "TStyle.h"
#include "TDirectory.h"
#include "TString.h"
// #include "LumiMap.h"
#include "map_byRun_2017_1.h"
// TString Run="324245";//"1";

Double_t rej = 6.;
Bool_t reject = kFALSE;

Double_t gaus2(Double_t *x, Double_t *par){
  if (reject && x[0] > -rej && x[0] < rej) {
    TF1::RejectPoint();
    return 0;
  }
  return TMath::Gaus(x[0],par[0],par[2],0)*par[4]+TMath::Gaus(x[0],par[1],par[3],0)*par[5]+par[6];
}

Double_t gaus4(Double_t *x, Double_t *par){
  if (reject && x[0] > -rej && x[0] < rej) {
    TF1::RejectPoint();
    return 0;
  }
  return TMath::Gaus(x[0],par[0],par[4],1)*par[8]+TMath::Gaus(x[0],par[1],par[5],1)*par[9]+
    TMath::Gaus(x[0],par[2],par[6],1)*par[10]+TMath::Gaus(x[0],par[3],par[7],1)*par[11]+par[12];
}

Double_t gaus3(Double_t *x, Double_t *par){
  if (reject && x[0] > -rej && x[0] < rej) {
    TF1::RejectPoint();
    return 0;
  }
  return TMath::Gaus(x[0],par[0],par[3],1)*par[6]+TMath::Gaus(x[0],par[1],par[4],1)*par[7]+TMath::Gaus(x[0],par[2],par[5],1)*par[8]+par[9];
}


// Student's t function:

Double_t normStud( Double_t *x, Double_t *par5 ) {

  static int nn = 0;
  nn++;
  static double dx = 0.1;
  static double b1 = 0;
  if( nn == 1 ) b1 = x[0];
  if( nn == 2 ) dx = x[0] - b1;
  //
  //--  Mean and width:
  //
  double xm = par5[0];
  double t = ( x[0] - xm ) / par5[1];
  double tt = t*t;
  //
  //--  exponent:
  //
  double rn = par5[2];
  double xn = 0.5 * ( rn + 1.0 );
  //
  //--  Normalization needs Gamma function:
  //
  double pk = 0.0;

  if( rn > 0.0 ) {

    double pi = 3.14159265358979323846;
    double aa = dx / par5[1] / sqrt(rn*pi) * TMath::Gamma(xn) / TMath::Gamma(0.5*rn);

    pk = par5[3] * aa * exp( -xn * log( 1.0 + tt/rn ) );
  }

  return pk + par5[4];
}

Double_t normGaus( Double_t *x, Double_t *par3) {

  if (par3[1] == 0) return 1.e30;
  Double_t arg = (x[0]-par3[0])/par3[1];
  Double_t res = TMath::Exp(-0.5*arg*arg);

  return par3[2] * (res/(2.50662827463100024*par3[1])); //sqrt(2*Pi)=2.50662827463100024
}

Double_t StudGaus( Double_t *x, Double_t *par8) {

  static int nn = 0;
  nn++;
  static double dx = 0.1;
  static double b1 = 0;
  if( nn == 1 ) b1 = x[0];
  if( nn == 2 ) dx = x[0] - b1;
  //
  //--  Mean and width:
  //
  double xm = par8[0];
  double t = ( x[0] - xm ) / par8[1];
  double tt = t*t;
  //
  //--  exponent:
  //
  double rn = par8[2];
  double xn = 0.5 * ( rn + 1.0 );
  //
  //--  Normalization needs Gamma function:
  //
  double pk = 0.0;

  if( rn > 0.0 ) {

    double pi = 3.14159265358979323846;
    double aa = dx / par8[1] / sqrt(rn*pi) * TMath::Gamma(xn) / TMath::Gamma(0.5*rn);

    pk = par8[3] * aa * exp( -xn * log( 1.0 + tt/rn ) );
  }

  if (par8[6] == 0) return 1.e30;
  Double_t arg = (x[0]-par8[5])/par8[6];
  Double_t res = TMath::Exp(-0.5*arg*arg);

  return (pk + par8[4]) + (par8[7] * (res/(2.50662827463100024*par8[6]))); //sqrt(2*Pi)=2.50662827463100024

}

Double_t doubleStud ( Double_t *x, Double_t *par9){

  static int nn = 0;
  nn++;
  static double dx = 0.1;
  static double b1 = 0;
  if( nn == 1 ) b1 = x[0];
  if( nn == 2 ) dx = x[0] - b1;
  //
  //--  Mean and width:
  //
  double xm = par9[0];
  double t = ( x[0] - xm ) / par9[1];
  double tt = t*t;
  //
  //--  exponent:
  //
  double rn = par9[2];
  double xn = 0.5 * ( rn + 1.0 );
  //
  //--  Normalization needs Gamma function:
  //
  double pk = 0.0;

  if( rn > 0.0 ) {

    double pi = 3.14159265358979323846;
    double aa = dx / par9[1] / sqrt(rn*pi) * TMath::Gamma(xn) / TMath::Gamma(0.5*rn);

    pk = par9[3] * aa * exp( -xn * log( 1.0 + tt/rn ) );
  }

  static int nn_2 = 0;
  nn_2++;
  static double dx_2 = 0.1;
  static double b1_2 = 0;
  if( nn_2 == 1 ) b1_2 = x[0];
  if( nn_2 == 2 ) dx_2 = x[0] - b1_2;
  //
  //--  Mean and width:
  //
  double xm_2 = par9[5];
  double t_2 = ( x[0] - xm_2 ) / par9[6];
  double tt_2 = t_2*t_2;
  //
  //--  exponent:
  //
  double rn_2 = par9[7];
  double xn_2 = 0.5 * ( rn_2 + 1.0 );
  //
  //--  Normalization needs Gamma function:
  //
  double pk_2 = 0.0;

  if( rn_2 > 0.0 ) {

    double pi = 3.14159265358979323846;
    double aa_2 = dx_2 / par9[6] / sqrt(rn_2*pi) * TMath::Gamma(xn_2) / TMath::Gamma(0.5*rn_2);

    pk_2 = par9[8] * aa_2 * exp( -xn_2 * log( 1.0 + tt_2/rn_2 ) );
  }

  return pk + par9[4] + pk_2;

}

Double_t tripleStud ( Double_t *x, Double_t *par13){

  static int nn = 0;
  nn++;
  static double dx = 0.1;
  static double b1 = 0;
  if( nn == 1 ) b1 = x[0];
  if( nn == 2 ) dx = x[0] - b1;
  //
  //--  Mean and width:
  //
  double xm = par13[0];
  double t = ( x[0] - xm ) / par13[1];
  double tt = t*t;
  //
  //--  exponent:
  //
  double rn = par13[2];
  double xn = 0.5 * ( rn + 1.0 );
  //
  //--  Normalization needs Gamma function:
  //
  double pk = 0.0;

  if( rn > 0.0 ) {

    double pi = 3.14159265358979323846;
    double aa = dx / par13[1] / sqrt(rn*pi) * TMath::Gamma(xn) / TMath::Gamma(0.5*rn);

    pk = par13[3] * aa * exp( -xn * log( 1.0 + tt/rn ) );
  }

  static int nn_2 = 0;
  nn_2++;
  static double dx_2 = 0.1;
  static double b1_2 = 0;
  if( nn_2 == 1 ) b1_2 = x[0];
  if( nn_2 == 2 ) dx_2 = x[0] - b1_2;
  //
  //--  Mean and width:
  //
  double xm_2 = par13[5];
  double t_2 = ( x[0] - xm_2 ) / par13[6];
  double tt_2 = t_2*t_2;
  //
  //--  exponent:
  //
  double rn_2 = par13[7];
  double xn_2 = 0.5 * ( rn_2 + 1.0 );
  //
  //--  Normalization needs Gamma function:
  //
  double pk_2 = 0.0;

  if( rn_2 > 0.0 ) {

    double pi = 3.14159265358979323846;
    double aa_2 = dx_2 / par13[6] / sqrt(rn_2*pi) * TMath::Gamma(xn_2) / TMath::Gamma(0.5*rn_2);

    pk_2 = par13[8] * aa_2 * exp( -xn_2 * log( 1.0 + tt_2/rn_2 ) );
  }

  static int nn_3 = 0;
  nn_3++;
  static double dx_3 = 0.1;
  static double b1_3 = 0;
  if( nn_3 == 1 ) b1_3 = x[0];
  if( nn_3 == 2 ) dx_3 = x[0] - b1_3;
  //
  //--  Mean and width:
  //
  double xm_3 = par13[9];
  double t_3 = ( x[0] - xm_3 ) / par13[10];
  double tt_3 = t_3*t_3;
  //
  //--  exponent:
  //
  double rn_3 = par13[11];
  double xn_3 = 0.5 * ( rn_3 + 1.0 );
  //
  //--  Normalization needs Gamma function:
  //
  double pk_3 = 0.0;

  if( rn_3 > 0.0 ) {

    double pi = 3.14159265358979323846;
    double aa_3 = dx_3 / par13[10] / sqrt(rn_3*pi) * TMath::Gamma(xn_3) / TMath::Gamma(0.5*rn_3);

    pk_3 = par13[12] * aa_3 * exp( -xn_3 * log( 1.0 + tt_3/rn_3 ) );
  }

  return pk + par13[4] + pk_2 + pk_3;

}

//
//----------------------------------------------------------------------
//

int fittp0(const char* hs , float & sigma_res,float & sigma_res_err , float & mean_res,float & mean_res_err, TString Run, TString reco) {

  TCanvas* c = new TCanvas("c","c",0,0,800,800);
  c->Draw();

  gROOT->Reset();
  gStyle->SetOptStat(0000);

  c->SetLeftMargin(0.15);

  TPad *pad = new TPad("pad","pad",0.15,0.01,0.99,0.99);
  pad->SetBottomMargin(0.18);
  pad->SetLeftMargin(0.15);
  //gPad->SetLogy();
  cout <<" Created pad for hist"<< hs  <<endl;

  TH1 *h = (TH1*)gDirectory->Get(hs);

  if( h == NULL ){
    cout << hs << " does not exist\n";
  }
  else{
    h->SetMarkerStyle(21);
    h->SetMarkerSize(0.8);

    h->SetTitle("");

    h->Rebin(30);
    TGaxis::SetMaxDigits(3);
    cout << "=====>" << h->GetBinWidth(1) << endl;
    double dx = h->GetBinWidth(1);
    double nmax = h->GetBinContent(h->GetMaximumBin());
    double xmax = h->GetBinCenter(h->GetMaximumBin());
    double nn = 7*nmax;

    int nb = h->GetNbinsX();
    double n1 = h->GetBinContent(1);
    double n9 = h->GetBinContent(nb);
    double bg = 0.5*(n1+n9);

    double x1 = h->GetBinCenter(1);
    double x9 = h->GetBinCenter(nb);

    TString name =  (TString) hs ;
    // create a TF1 with the range from x1 to x9 and 5 parameters

    TF1 *tp0Fcn ;
    //fit = "single Student-t fit";
    tp0Fcn = new TF1( "tp0Fcn", normStud, x1, x9, 5 );

    tp0Fcn->SetParName( 0, "mean" );
    tp0Fcn->SetParName( 1, "sigma" );
    tp0Fcn->SetParName( 2, "nu" );
    tp0Fcn->SetParName( 3, "area" );
    tp0Fcn->SetParName( 4, "BG" );

    tp0Fcn->SetNpx(500);
    tp0Fcn->SetLineWidth(4);
    tp0Fcn->SetLineColor(kGreen);
    tp0Fcn->SetLineColor(kGreen);

    // set start values for some parameters:

    tp0Fcn->SetParameter( 0, 0.);//xmax ); // peak position
    tp0Fcn->SetParameter( 1, 4*dx ); // width
    tp0Fcn->SetParameter( 2, 2.2 ); // nu
    tp0Fcn->SetParameter( 3, nn ); // N
    tp0Fcn->SetParameter( 4, bg );
    //h->Scale(1/h->Integral());
    h->Draw();
    h->Fit( "tp0Fcn", "RN", "ep" );
    // h->Fit("tp0Fcn","V+","ep");

    sigma_res= tp0Fcn->GetParameter(1);
    sigma_res_err= tp0Fcn->GetParError(1);
    mean_res= tp0Fcn->GetParameter(0);
    mean_res_err= tp0Fcn->GetParError(0);

    std::cout <<  hs << ": mean " <<mean_res << " +-"  << mean_res_err   << " sigma "<< sigma_res << " +-"  << sigma_res_err  <<std::endl;
    std::cout << tp0Fcn->GetParameter(1) << " " << tp0Fcn->GetParameter(3) << " " << tp0Fcn->GetParameter(6) << " " << tp0Fcn->GetParameter(8) << endl;
    std::cout << "*************"<<std::endl;

    TLegend *pl2 = new TLegend(0.55,0.54,0.65,0.89);
    pl2->SetTextSize(0.035);
    pl2->SetFillColor(0);
    pl2->SetBorderSize(0);

    std::ofstream outfile;
    //TString name_of_text_file = (TString)"Param_"+Run+(TString)".txt";
    //outfile.open(name_of_text_file.Data(), std::ios_base::app);
    cout << "========>" << name << endl;

    // if(strstr(name, "0f2") != NULL)   outfile << "D1, x, sigma, delta_sigma, mu, delta_mu, RMS, delta_RMS, " << HV_val << ": ";
    // if(strstr(name, "0f3") != NULL)   outfile << "D2, x, sigma, delta_sigma, mu, delta_mu, RMS, delta_RMS, " << HV_val << ": ";
    // if(strstr(name, "0f4") != NULL)   outfile << "D3, x, sigma, delta_sigma, mu, delta_mu, RMS, delta_RMS, " << HV_val << ": ";
    // if(strstr(name, "1f2") != NULL)   outfile << "D1, y, sigma, delta_sigma, mu, delta_mu, RMS, delta_RMS, " << HV_val << ": ";
    // if(strstr(name, "1f3") != NULL)   outfile << "D2, y, sigma, delta_sigma, mu, delta_mu, RMS, delta_RMS, " << HV_val << ": ";
    // if(strstr(name, "1f4") != NULL)   outfile << "D3, y, sigma, delta_sigma, mu, delta_mu, RMS, delta_RMS, " << HV_val << ": ";

    //outfile << sigma_res << ", " << sigma_res_err << ", " << mean_res << ", " << mean_res_err << ", " << h->GetRMS() <<  ", " << h->GetRMSError() << std::endl;

    if ( name.Contains("h_dx_1") || name.Contains("h_dz_1") )  pl2->SetHeader("Barrel Pixel Layer 1");
    if ( name.Contains("h_dx_2") || name.Contains("h_dz_2") )  pl2->SetHeader("Barrel Pixel Layer 2");
    if ( name.Contains("h_dx_3") || name.Contains("h_dz_3") )  pl2->SetHeader("Barrel Pixel Disk 3");
    if ( name.Contains("h_dx_4") || name.Contains("h_dz_4") )  pl2->SetHeader("Barrel Pixel Disk 4");

    TLegendEntry *ple2 = pl2->AddEntry(h, "Triplet Residuals",  "P");
    TLegendEntry *ple4 = pl2->AddEntry((TObject*)0, "#mu_{r}="+TString::Format("%.2f",mean_res )+"#pm"+ TString::Format("%.2f",mean_res_err )  +" #mum",  "");
    ple4->SetTextColor(kRed);
    TLegendEntry *ple3 = pl2->AddEntry((TObject*)0, "#sigma_{r}="+TString::Format("%.2f",sigma_res )+"#pm"+ TString::Format("%.2f",sigma_res_err )  +" #mum",  "");
    TLegendEntry *ple5=  pl2->AddEntry((TObject*)0, "mean="+TString::Format("%.2f",h->GetMean())+ "#pm"+TString::Format("%.2f",h->GetMeanError() )+" #mum",  "");
    TLegendEntry *ple6=  pl2->AddEntry((TObject*)0, "RMS="+TString::Format("%.2f",h->GetRMS())+"#pm"+ TString::Format("%.2f",h->GetRMSError() ) + " #mum",  "");

    ple3->SetTextColor(kRed);
    ple5->SetTextColor(kRed);
    ple6->SetTextColor(kRed);

    pl2->Draw("same");

    h->GetYaxis()->SetTitle("Number of hits / "+ TString::Format("%.0f",dx) +" #mum");
    if ( name.Contains("dx")) h->GetXaxis()->SetTitle("Residuals x direction (#mum)");
    else if ( name.Contains("dz"))  h->GetXaxis()->SetTitle("Residuals y direction (#mum)");

    h->GetXaxis()->SetTitleSize(0.06);
    h->GetYaxis()->SetTitleSize(0.06);
    h->GetYaxis()->SetTitleOffset(1.2);
    h->GetXaxis()->SetTitleOffset(0.7);
    h->GetXaxis()->SetLabelSize(0.045);
    h->GetYaxis()->SetLabelSize(0.045);
    //h->GetXaxis()->SetRangeUser(-10,10);

    TString cmsText     = "CMS";
    float cmsTextFont   = 61;  // default is helvetic-bold
    bool writeExtraText = true;
    TString extraText   ="Work in Progress 2018";// Phase1";
    if ( Run=="1")extraText   = "Simulation 2018";// Phase1";

    float extraTextFont = 52;  // default is helvetica-italics
    // text sizes and text offsets with respect to the top frame in unit of the top margin size
    float lumiTextSize     = 0.5;
    float lumiTextOffset   = 0.15;
    float cmsTextSize      = 0.65;
    float cmsTextOffset    = 0.1;  // only used in outOfFrame version
    float relPosX    = 0.045;
    float relPosY    = 0.035;
    float relExtraDY = 1.2;
    // ratio of "CMS" and extra text size
    float extraOverCmsTextSize  = 0.65;
    TString lumi_13TeV = "20.1 fb^{-1}";
    TString lumi_8TeV  = "19.7 fb^{-1}";
    TString lumi_7TeV  = "5.1 fb^{-1}";
    TString lumiText;
    // lumiText += lumi_8TeV;
    // lumiText += " (13 TeV)";
    lumiText = "(13 TeV)";
    float t = pad->GetTopMargin();
    float b = pad->GetBottomMargin();
    float r = pad->GetRightMargin();
    float l = pad->GetLeftMargin();
    TLatex latex;
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(kBlack);
    float extraTextSize = extraOverCmsTextSize*cmsTextSize;
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(lumiTextSize*t*0.90);
    latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText);
    latex.SetTextFont(cmsTextFont);
    latex.SetTextAlign(11);
    latex.SetTextSize(cmsTextSize*t);
    latex.DrawLatex(l+0.09,1-t+lumiTextOffset*t,cmsText);
    latex.SetTextFont(extraTextFont);
    latex.SetTextSize(extraTextSize*t);
    latex.DrawLatex(l+0.23, 1-t+lumiTextOffset*t, extraText);

    //    TString TrackRecoText = "Generic reconstruction";
    TString TrackRecoText = reco+" reconstruction";
    latex.SetTextFont(42);
    latex.SetTextSize(extraTextSize*t*0.93);
    latex.DrawLatex(l+0.02, 1-t+lumiTextOffset*t-0.09, TrackRecoText);


    TString TrackSelctionText = "Track p_{T} > 12 GeV";
    latex.SetTextFont(42);
    latex.SetTextSize(extraTextSize*t*0.93);
    latex.DrawLatex(l+0.02, 1-t+lumiTextOffset*t-0.14, TrackSelctionText);

    TString RunText = "Run: " + (TString) Run;
    latex.SetTextFont(42);
    latex.SetTextSize(extraTextSize*t*0.75);
    //latex.DrawLatex(l+0.03, 1-t+lumiTextOffset*t-0.09-0.06-0.18, RunText);

    // TString HVText = "HV = "+ (TString)HV_val+"V";
    latex.SetTextFont(42);
    latex.SetTextSize(extraTextSize*t*0.75);
    //latex.DrawLatex(l+0.03, 1-t+lumiTextOffset*t-0.09-0.06-0.25, HVText);

    h->Draw("hist ep same"); // data again on top
    // gPad->Print(hs+".png");
    gPad->RedrawAxis("same");
    c->Update();
    h->SetMaximum(tp0Fcn->GetMaximum() * 1.5);
    h->Draw("hist ep same");

    //c->Update();

    name +=(TString) "_"+Run+(TString)"_" +(TString)"_"+reco+"_tree.pdf" ;
    TString name_png = (TString) hs ;
    TString name_eps = (TString) hs ;
    name_png +=(TString) "_"+Run+(TString)"_" +  (TString)"_"+reco+"_tree.png";
    name_eps +=(TString) "_"+Run+(TString)"_" +  (TString)"_"+reco+"_tree.eps" ;

    c->SaveAs((TString)"Test_"+reco+"/"+name);
    c->SaveAs((TString)"Test_"+reco+"/"+name_png);
    c->SaveAs((TString)"Test_"+reco+"/"+name_eps);

    // gPad->Print(name);
    //delete tp0Fcn;
  }
 return 0;

}

template < typename T>

std::pair<bool, int > findInVector(const std::vector<T>  & vecOfElements, const T  & element)
{
	std::pair<bool, int > result;

	// Find given element in vector
	auto it = std::find(vecOfElements.begin(), vecOfElements.end(), element);

	if (it != vecOfElements.end())
	{
		result.second = distance(vecOfElements.begin(), it);
		result.first = true;
	}
	else
	{
		result.first = false;
		result.second = -1;
	}

	return result;
}

std::map<int, std::map<TString, float>> FitAndPlot(const char *path, vector<int> Runs, TString reco = "Template")
{
  std::cout << "Loading file collection from " << path << std::endl;
  TFileCollection fc("","",path);
  // TFileCollection fc("","","UL_2017G_test.txt");
  std::cout << "Files found : " << fc.GetNFiles() << std::endl;
  //TString treePath = "BPixResolution_Template/tree";
  TString treePath = "BPixResolution_"+reco+"/tree";
  TChain chain(treePath);

  chain.AddFileInfoList(fc.GetList());
  int nEvents = (int)chain.GetEntries();
  cout << "nEvents : " << nEvents << endl;

  vector< float >  * dx_1 = nullptr;
  vector< float >  * dz_1 = nullptr;
  vector< float >  * dx_2 = nullptr;
  vector< float >  * dz_2 = nullptr;
  vector< float >  * dx_3 = nullptr;
  vector< float >  * dz_3 = nullptr;
  vector< float >  * dx_4 = nullptr;
  vector< float >  * dz_4 = nullptr;

  chain.SetBranchAddress("dx_resolution_study_l1", &dx_1);
  chain.SetBranchAddress("dz_resolution_study_l1", &dz_1);
  chain.SetBranchAddress("dx_resolution_study_l2", &dx_2);
  chain.SetBranchAddress("dz_resolution_study_l2", &dz_2);
  chain.SetBranchAddress("dx_resolution_study_l3", &dx_3);
  chain.SetBranchAddress("dz_resolution_study_l3", &dz_3);
  chain.SetBranchAddress("dx_resolution_study_l4", &dx_4);
  chain.SetBranchAddress("dz_resolution_study_l4", &dz_4);

  vector< float > *pt = nullptr;
  chain.SetBranchAddress("pt_resolution_study", &pt);

  vector< float > *measl = nullptr;
  chain.SetBranchAddress("layers_with_measurement", &measl);

  int RunNumber=-1, LumiNumber=-1;

  vector <Int_t> LSMinArr = {0};
  vector <Int_t> LSMaxArr = {1000000};

  chain.SetBranchAddress("runNumber_res",&RunNumber);
  chain.SetBranchAddress("lumiBlock_res", &LumiNumber);

  // TH1F *h_dx_1[Runs.size()];// = new TH1F("h_dx_1", "FPix disk 1, x direction", 3000, -150, +150);
  // TH1F *h_dz_1[Runs.size()];// = new TH1F("h_dz_1", "FPix disk 1, y direction", 3000, -300, +300);
  // TH1F *h_dx_2[Runs.size()];// = new TH1F("h_dx_2", "FPix disk 2, x direction", 3000, -150, +150);
  // TH1F *h_dz_2[Runs.size()];// = new TH1F("h_dz_2", "FPix disk 2, y direction", 3000, -300, +300);
  // TH1F *h_dx_3[Runs.size()];// = new TH1F("h_dx_3", "FPix disk 3, x direction", 3000, -150, +150);
  // TH1F *h_dz_3[Runs.size()];// = new TH1F("h_dz_3", "FPix disk 3, y direction", 3000, -300, +300);
  // TH1F *h_dx_4[Runs.size()];// = new TH1F("h_dx_3", "FPix disk 3, x direction", 3000, -150, +150);
  // TH1F *h_dz_4[Runs.size()];// = new TH1F("h_dz_3", "FPix disk 3, y direction", 3000, -300, +300);

  //sigma
  std::map <int, TH1F> h_dx_1_map;
  std::map <int, TH1F> h_dz_1_map;
  std::map <int, TH1F> h_dx_2_map;
  std::map <int, TH1F> h_dz_2_map;
  std::map <int, TH1F> h_dx_3_map;
  std::map <int, TH1F> h_dz_3_map;
  std::map <int, TH1F> h_dx_4_map;
  std::map <int, TH1F> h_dz_4_map;

  for(auto const& r: Runs){
    h_dx_1_map[r] = TH1F("h_dx_1_"+TString::Itoa(r,10), "BPix layer 1, x direction", 3000, -150, +150);
    h_dz_1_map[r] = TH1F("h_dz_1_"+TString::Itoa(r,10), "BPix layer 1, y direction", 3000, -300, +300);
    h_dx_2_map[r] = TH1F("h_dx_2_"+TString::Itoa(r,10), "BPix layer 2, x direction", 3000, -150, +150);
    h_dz_2_map[r] = TH1F("h_dz_2_"+TString::Itoa(r,10), "BPix layer 2, y direction", 3000, -300, +300);
    h_dx_3_map[r] = TH1F("h_dx_3_"+TString::Itoa(r,10), "BPix layer 3, x direction", 3000, -150, +150);
    h_dz_3_map[r] = TH1F("h_dz_3_"+TString::Itoa(r,10), "BPix layer 3, y direction", 3000, -300, +300);
    h_dx_4_map[r] = TH1F("h_dx_4_"+TString::Itoa(r,10), "BPix layer 4, x direction", 3000, -150, +150);
    h_dz_4_map[r] = TH1F("h_dz_4_"+TString::Itoa(r,10), "BPix layer 4, y direction", 3000, -300, +300);
  }
  // TH1F *h_dx_1 = new TH1F("h_dx_1_"+TString::Itoa(Run,10), "BPix layer 1, x direction", 3000, -150, +150);
  // TH1F *h_dz_1 = new TH1F("h_dz_1_"+TString::Itoa(Run,10), "BPix layer 1, y direction", 3000, -300, +300);
  // TH1F *h_dx_2 = new TH1F("h_dx_2_"+TString::Itoa(Run,10), "BPix layer 2, x direction", 3000, -150, +150);
  // TH1F *h_dz_2 = new TH1F("h_dz_2_"+TString::Itoa(Run,10), "BPix layer 2, y direction", 3000, -300, +300);
  // TH1F *h_dx_3 = new TH1F("h_dx_3_"+TString::Itoa(Run,10), "BPix layer 3, x direction", 3000, -150, +150);
  // TH1F *h_dz_3 = new TH1F("h_dz_3_"+TString::Itoa(Run,10), "BPix layer 3, y direction", 3000, -300, +300);
  // TH1F *h_dx_4 = new TH1F("h_dx_4_"+TString::Itoa(Run,10), "BPix layer 4, x direction", 3000, -150, +150);
  // TH1F *h_dz_4 = new TH1F("h_dz_4_"+TString::Itoa(Run,10), "BPix layer 4, y direction", 3000, -300, +300);
  //nEvents = 1000;
  for(int j=0; j<nEvents; j++ ){
    chain.GetEntry(j);
    // std::pair<bool, int> result = findInVector<int>(Runs, round(RunNumber)/1);
    if ((j+1) % 10000 == 0){
       cout << "processed " << 100.*(double)((double)j/(double)nEvents) << "% of events" << endl;
    }
    // if (!result.first) continue;
    // if ((int)RunNumber != (int)Run) continue;
    // if(LumiNumber<LSMinArr[result.second] || LumiNumber>LSMaxArr[result.second]) continue;

    int size_pt = pt->size();
    for(int i=0; i<size_pt; i++){
      if(pt->at(i)>12.){
      	h_dx_1_map[RunNumber].Fill(dx_1->at(i));
      	h_dz_1_map[RunNumber].Fill(dz_1->at(i));
      	h_dx_2_map[RunNumber].Fill(dx_2->at(i));
      	h_dz_2_map[RunNumber].Fill(dz_2->at(i));
      	h_dx_3_map[RunNumber].Fill(dx_3->at(i));
      	h_dz_3_map[RunNumber].Fill(dz_3->at(i));
      	h_dx_4_map[RunNumber].Fill(dx_4->at(i));
      	h_dz_4_map[RunNumber].Fill(dz_4->at(i));
      }
    }
  }

  std::map<int, std::map<TString, float>> outmap;

  for(auto const& Run: Runs){
    float sigma_x1,sigma_x1_err,mean_x1,mean_x1_err ;
    fittp0("h_dx_1_"+TString::Itoa(Run,10),sigma_x1,sigma_x1_err,mean_x1,mean_x1_err, (TString)Run, reco);

    float sigma_z1,sigma_z1_err,mean_z1,mean_z1_err ;
    fittp0("h_dz_1_"+TString::Itoa(Run,10),sigma_z1,sigma_z1_err,mean_z1,mean_z1_err, (TString)Run, reco);

    float sigma_x2,sigma_x2_err,mean_x2,mean_x2_err ;
    fittp0("h_dx_2_"+TString::Itoa(Run,10),sigma_x2,sigma_x2_err,mean_x2,mean_x2_err, (TString)Run, reco);

    float sigma_z2,sigma_z2_err,mean_z2,mean_z2_err ;
    fittp0("h_dz_2_"+TString::Itoa(Run,10),sigma_z2,sigma_z2_err,mean_z2,mean_z2_err, (TString)Run, reco);

    float sigma_x3,sigma_x3_err,mean_x3,mean_x3_err ;
    fittp0("h_dx_3_"+TString::Itoa(Run,10),sigma_x3,sigma_x3_err,mean_x3,mean_x3_err, (TString)Run, reco);

    float sigma_z3,sigma_z3_err,mean_z3,mean_z3_err ;
    fittp0("h_dz_3_"+TString::Itoa(Run,10),sigma_z3,sigma_z3_err,mean_z3,mean_z3_err, (TString)Run, reco);

    float sigma_x4,sigma_x4_err,mean_x4,mean_x4_err ;
    fittp0("h_dx_4_"+TString::Itoa(Run,10),sigma_x4,sigma_x4_err,mean_x4,mean_x4_err, (TString)Run, reco);

    float sigma_z4,sigma_z4_err,mean_z4,mean_z4_err ;
    fittp0("h_dz_4_"+TString::Itoa(Run,10),sigma_z4,sigma_z4_err,mean_z4,mean_z4_err, (TString)Run, reco);
  

    cout << "Run "+TString::Itoa(Run,10)+" has beed processed successfully!" << endl;
  
    cout << "1" << endl;
    outmap[Run][TString("sigma_x1"     )] =  sigma_x1    ;
    outmap[Run][TString("sigma_x1_err" )] =  sigma_x1_err;
    outmap[Run][TString("sigma_z1"     )] =  sigma_z1    ;
    outmap[Run][TString("sigma_z1_err" )] =  sigma_z1_err;
    outmap[Run][TString("sigma_x2"     )] =  sigma_x2    ;
    outmap[Run][TString("sigma_x2_err" )] =  sigma_x2_err;
    outmap[Run][TString("sigma_z2"     )] =  sigma_z2    ;
    outmap[Run][TString("sigma_z2_err" )] =  sigma_z2_err;
    outmap[Run][TString("sigma_x3"     )] =  sigma_x3    ;
    outmap[Run][TString("sigma_x3_err" )] =  sigma_x3_err;
    outmap[Run][TString("sigma_z3"     )] =  sigma_z3    ;
    outmap[Run][TString("sigma_z3_err" )] =  sigma_z3_err;
    outmap[Run][TString("sigma_x4"     )] =  sigma_x4    ;
    outmap[Run][TString("sigma_x4_err" )] =  sigma_x4_err;
    outmap[Run][TString("sigma_z4"     )] =  sigma_z4    ;
    outmap[Run][TString("sigma_z4_err" )] =  sigma_z4_err;

    outmap[Run][TString("mean_x1"     )] =  mean_x1    ;
    outmap[Run][TString("mean_x1_err" )] =  mean_x1_err;
    outmap[Run][TString("mean_z1"     )] =  mean_z1    ;
    outmap[Run][TString("mean_z1_err" )] =  mean_z1_err;
    outmap[Run][TString("mean_x2"     )] =  mean_x2    ;
    outmap[Run][TString("mean_x2_err" )] =  mean_x2_err;
    outmap[Run][TString("mean_z2"     )] =  mean_z2    ;
    outmap[Run][TString("mean_z2_err" )] =  mean_z2_err;
    outmap[Run][TString("mean_x3"     )] =  mean_x3    ;
    outmap[Run][TString("mean_x3_err" )] =  mean_x3_err;
    outmap[Run][TString("mean_z3"     )] =  mean_z3    ;
    outmap[Run][TString("mean_z3_err" )] =  mean_z3_err;
    outmap[Run][TString("mean_x4"     )] =  mean_x4    ;
    outmap[Run][TString("mean_x4_err" )] =  mean_x4_err;
    outmap[Run][TString("mean_z4"     )] =  mean_z4    ;
    outmap[Run][TString("mean_z4_err" )] =  mean_z4_err;
  }
  // cout << "2" << endl;
  return outmap;
}
// vector <Int_t> Runs = {297050, 297056, 297057, 297099, 297100, 297101, 297113, 297114, 297175, 297176, 297177, 297178, 297215, 297218, 297219, 297224, 297225, 297227, 297292, 297293, 297296, 297308, 297359, 297411, 297424, 297425, 297426, 297429, 297430, 297431, 297432, 297433, 297434, 297435, 297467, 297468, 297469, 297483, 297484, 297485, 297486, 297487, 297488, 297503, 297504, 297505, 297557, 297558, 297562, 297563, 297598, 297599, 297603, 297604, 297605, 297606, 297620, 297656, 297665, 297666, 297670, 297674, 297675, 297722, 297723, 298996, 298997, 299000, 299042, 299061, 299062, 299064, 299065, 299067, 299096, 299149, 299178, 299180, 299184, 299185, 299327, 299329};
void FitAndPlot_tree_bpix_new(TString run, TString reco){
  int Run = run.Atoi();
  // ofstream file_dx_1, file_dx_2, file_dx_3, file_dx_4, file_dz_1, file_dz_2, file_dz_3, file_dz_4;
  ofstream file_x_1, file_x_2, file_x_3, file_x_4, file_z_1, file_z_2, file_z_3, file_z_4;

  // file_dx_1.open("Test_"+reco+"/"+"dx_1_"+reco+run+".txt", std::ios_base::app);
  // file_dx_2.open("Test_"+reco+"/"+"dx_2_"+reco+run+".txt", std::ios_base::app);
  // file_dx_3.open("Test_"+reco+"/"+"dx_3_"+reco+run+".txt", std::ios_base::app);
  // file_dx_4.open("Test_"+reco+"/"+"dx_4_"+reco+run+".txt", std::ios_base::app);
  // file_dz_1.open("Test_"+reco+"/"+"dz_1_"+reco+run+".txt", std::ios_base::app);
  // file_dz_2.open("Test_"+reco+"/"+"dz_2_"+reco+run+".txt", std::ios_base::app);
  // file_dz_3.open("Test_"+reco+"/"+"dz_3_"+reco+run+".txt", std::ios_base::app);
  // file_dz_4.open("Test_"+reco+"/"+"dz_4_"+reco+run+".txt", std::ios_base::app);

  file_x_1.open("Test_"+reco+"/"+"x_1_"+reco+run+".txt", std::ios_base::app);
  file_x_2.open("Test_"+reco+"/"+"x_2_"+reco+run+".txt", std::ios_base::app);
  file_x_3.open("Test_"+reco+"/"+"x_3_"+reco+run+".txt", std::ios_base::app);
  file_x_4.open("Test_"+reco+"/"+"x_4_"+reco+run+".txt", std::ios_base::app);
  file_z_1.open("Test_"+reco+"/"+"z_1_"+reco+run+".txt", std::ios_base::app);
  file_z_2.open("Test_"+reco+"/"+"z_2_"+reco+run+".txt", std::ios_base::app);
  file_z_3.open("Test_"+reco+"/"+"z_3_"+reco+run+".txt", std::ios_base::app);
  file_z_4.open("Test_"+reco+"/"+"z_4_"+reco+run+".txt", std::ios_base::app);

  std::map<int, std::map<TString, float>> outmap;

  // int Run;
  // char *path;
  // for(int i = 0; i < Runs.size(); i++){
    // Run = Runs[i];
  TString pathTstr = "/afs/cern.ch/user/d/dbrzhech/ServiceWork/BPixResolution/CMSSW_11_1_0_pre1/src/DPGAnalysis-SiPixelTools/PixelTriplets/file_lists_alcareco/" + run + ".txt";
  const char *path = pathTstr.Data();
  std::map<TString, vector<int>> Run_map;
  
  Run_map["runb2017"] = {
            297047,297050,297056,297057,297099,297100,297101,297113,297114,297168,297169,297170,
            297171,297175,297176,297177,297178,297179,297180,297181,297211,297215,297218,297219,
            297224,297225,297227,297281,297286,297292,297293,297296,297308,297359,297411,297424,
            297425,297426,297429,297430,297431,297432,297433,297434,297435,297467,297468,297469,
            297474,297483,297484,297485,297486,297487,297488,297503,297504,297505,297557,297558,
            297562,297563,297598,297599,297603,297604,297605,297606,297620,297656,297659,297660,
            297664,297665,297666,297670,297671,297672,297674,297675,297678,297722,297723,298678,
            298996,298997,298998,299000,299042,299061,299062,299064,299065,299067,299096,299149,
            299178,299180,299184,299185,299316,299317,299318,299324,299325,299326,299327,299329};
  Run_map["runc2017"] = {
            299368,299369,299370,299380,299381,299394,299395,299396,299420,299443,299450,299477,
            299478,299479,299480,299481,299592,299593,299594,299595,299597,299614,299616,299617,
            299649,300079,300087,300105,300106,300107,300117,300122,300123,300124,300155,300156,
            300157,300226,300233,300234,300235,300236,300237,300238,300239,300240,300280,300281,
            300282,300283,300284,300364,300365,300366,300367,300368,300369,300370,300371,300372,
            300373,300374,300375,300389,300390,300391,300392,300393,300394,300395,300396,300397,
            300398,300399,300400,300401,300459,300461,300462,300463,300464,300466,300467,300497,
            300498,300499,300500,300514,300515,300516,300517,300538,300539,300545,300548,300551,
            300552,300558,300560,300574,300575,300576,300631,300632,300633,300635,300636,300673,
            300674,300675,300676,300742,300777,300780,300785,300806,300811,300812,300816,300817,
            301046,301086,301141,301142,301161,301165,301179,301180,301183,301281,301283,301298,
            301323,301330,301359,301383,301384,301391,301392,301393,301394,301395,301396,301397,
            301398,301399,301417,301447,301448,301449,301450,301461,301472,301473,301474,301475,
            301476,301480,301519,301524,301525,301526,301528,301529,301530,301531,301532,301567,
            301627,301664,301665,301694,301912,301913,301914,301941,301959,301960,301969,301970,
            301984,301985,301986,301987,301997,301998,302019,302026,302029};
  Run_map["rund2017"] = {
            302031,302033,302034,302036,302037,302038,302040,302041,302042,302043,302131,302159,
            302163,302165,302166,302225,302228,302229,302239,302240,302262,302263,302277,302279,
            302280,302322,302328,302337,302342,302343,302344,302349,302350,302388,302392,302393,
            302448,302472,302473,302474,302475,302476,302479,302484,302485,302486,302487,302488,
            302490,302491,302492,302493,302494,302509,302513,302522,302523,302524,302525,302526,
            302548,302550,302551,302553,302554,302555,302563,302564,302565,302566,302567,302570,
            302571,302572,302573,302596,302597,302634,302635,302646,302651,302654,302660,302661,
            302663};
  Run_map["runa2018"] = {
            315257,315258,315259,315264,315265,315267,315270,315322,315339,315357,315361,315363,
            315365,315366,315420,315488,315489,315490,315506,315509,315510,315512,315543,315555,
            315556,315557,315640,315641,315642,315644,315645,315646,315647,315648,315689,315690,
            315702,315703,315704,315705,315713,315721,315741,315764,315770,315784,315785,315786,
            315788,315789,315790,315800,315801,315840,315973,315974,316058,316059,316060,316061,
            316062,316082,316109,316110,316111,316112,316113,316114,316151,316153,316186,316187,
            316199,316200,316201,316202,316216,316217,316218,316219,316239,316240,316241,316271,
            316361,316362,316363,316377,316378,316379,316380,316455,316456,316457,316469,316470,
            316472,316505,316569,316590,316613,316615,316664,316665,316666,316667,316700,316701,
            316702,316715,316716,316717,316718,316719,316720,316721,316722,316723,316758,316766,
            316876,316877,316879,316928,316944,316985,316993,316994,316995};
  Run_map["runb2018"] = {
            317080,317087,317088,317089,317182,317212,317213,317279,317291,317292,317295,317296,
            317297,317319,317320,317338,317339,317340,317382,317383,317391,317392,317434,317435,
            317438,317475,317478,317479,317480,317481,317482,317484,317488,317509,317510,317511,
            317512,317527,317591,317626,317640,317641,317648,317649,317650,317661,317663,317683,
            317696,318733,318816,318819,318820,318828,318872,318874,318876,318877,318944,319077,
            319310};
  Run_map["rund2018"] = {
            320500,320569,320570,320571,320673,320674,320688,320712,320757,320804,320807,320809,
            320821,320822,320823,320824,320838,320840,320841,320853,320854,320855,320856,320857,
            320858,320859,320887,320888,320916,320917,320920,320933,320934,320936,320941,320980,
            320995,320996,321004,321005,321006,321007,321009,321010,321011,321012,321051,321055,
            321067,321068,321069,321119,321121,321122,321123,321124,321126,321134,321138,321140,
            321149,321162,321164,321165,321166,321167,321177,321178,321218,321219,321221,321230,
            321231,321232,321233,321261,321262,321283,321294,321295,321296,321305,321310,321311,
            321312,321313,321393,321396,321397,321414,321415,321431,321432,321433,321434,321436,
            321457,321461,321475,321709,321710,321712,321730,321731,321732,321735,321755,321758,
            321759,321760,321773,321774,321775,321776,321777,321778,321780,321781,321794,321796,
            321813,321815,321817,321818,321819,321820,321831,321832,321833,321834,321879,321880,
            321887,321908,321909,321917,321919,321933,321960,321961,321973,321975,321988,321990,
            322013,322014,322022,322040,322057,322068,322079,322088,322106,322113,322118,322179,
            322201,322204,322222,322252,322317,322319,322322,322324,322332,322348,322355,322356,
            322381,322407,322430,322431,322480,322483,322484,322485,322487,322492,322510,322599,
            322602,322603,322605,322616,322617,322625,322633,323413,323414,323416,323417,323418,
            323419,323420,323421,323422,323423,323470,323471,323472,323473,323474,323475,323487,
            323488,323492,323493,323495,323524,323525,323526,323693,323696,323702,323725,323726,
            323727,323755,323775,323778,323790,323794,323841,323857,323940,323954,323976,323978,
            323980,323983,323997,324021,324022,324077,324201,324202,324205,324206,324207,324209,
            324237,324245,324293,324315,324318,324420,324564,324570,324571,324729,324747,324764,
            324765,324769,324772,324785,324791,324835,324840,324841,324846,324878,324897,324970,
            324980,324997,324998,324999,325000,325001,325022,325057,325097,325098,325099,325100,
            325101,325110,325111,325113,325114,325117,325159,325168,325169,325170,325172,325175};
  outmap = FitAndPlot(path, Run_map[run], reco);
  // cout << "2" << endl;
  // float Lumi = runToLumi(Run);
  // float Lumi = runToLumi(Run);
  // cout << "2.5" << endl;
  std::map<TString, float> outmaprun;
  for(auto const& Run: Run_map[run]){
    outmaprun = outmap[Run];
    // file_dx_1 << Run << "\t" << outmaprun[TString("sigma_x1")] << "\t" <<  outmaprun[TString("sigma_x1_err")] << endl;
    // file_dx_2 << Run << "\t" << outmaprun[TString("sigma_x2")] << "\t" <<  outmaprun[TString("sigma_x2_err")] << endl;
    // file_dx_3 << Run << "\t" << outmaprun[TString("sigma_x3")] << "\t" <<  outmaprun[TString("sigma_x3_err")] << endl;
    // file_dx_4 << Run << "\t" << outmaprun[TString("sigma_x4")] << "\t" <<  outmaprun[TString("sigma_x4_err")] << endl;
    // file_dz_1 << Run << "\t" << outmaprun[TString("sigma_z1")] << "\t" <<  outmaprun[TString("sigma_z1_err")] << endl;
    // file_dz_2 << Run << "\t" << outmaprun[TString("sigma_z2")] << "\t" <<  outmaprun[TString("sigma_z2_err")] << endl;
    // file_dz_3 << Run << "\t" << outmaprun[TString("sigma_z3")] << "\t" <<  outmaprun[TString("sigma_z3_err")] << endl;
    // file_dz_4 << Run << "\t" << outmaprun[TString("sigma_z4")] << "\t" <<  outmaprun[TString("sigma_z4_err")] << endl;
    
    file_x_1 << Run << "\t" << outmaprun[TString("mean_x1")] << "\t" <<  outmaprun[TString("mean_x1_err")] << endl;
    file_x_2 << Run << "\t" << outmaprun[TString("mean_x2")] << "\t" <<  outmaprun[TString("mean_x2_err")] << endl;
    file_x_3 << Run << "\t" << outmaprun[TString("mean_x3")] << "\t" <<  outmaprun[TString("mean_x3_err")] << endl;
    file_x_4 << Run << "\t" << outmaprun[TString("mean_x4")] << "\t" <<  outmaprun[TString("mean_x4_err")] << endl;
    file_z_1 << Run << "\t" << outmaprun[TString("mean_z1")] << "\t" <<  outmaprun[TString("mean_z1_err")] << endl;
    file_z_2 << Run << "\t" << outmaprun[TString("mean_z2")] << "\t" <<  outmaprun[TString("mean_z2_err")] << endl;
    file_z_3 << Run << "\t" << outmaprun[TString("mean_z3")] << "\t" <<  outmaprun[TString("mean_z3_err")] << endl;
    file_z_4 << Run << "\t" << outmaprun[TString("mean_z4")] << "\t" <<  outmaprun[TString("mean_z4_err")] << endl;
  }
  // }
  // cout << "3" << endl;
  // file_dx_1.close();
  // file_dx_2.close();
  // file_dx_3.close();
  // file_dx_4.close();
  // file_dz_1.close();
  // file_dz_2.close();
  // file_dz_3.close();
  // file_dz_4.close();

  file_x_1.close();
  file_x_2.close();
  file_x_3.close();
  file_x_4.close();
  file_z_1.close();
  file_z_2.close();
  file_z_3.close();
  file_z_4.close();

  //vector <Int_t> Runs = {304292};
  //{297020,297031,297039,297046,297047,297048,297049,297050,297056,297057,297065,297067,297068,297099,297100,297101,297107,297112,297113,297114,297116,297150,297160,297161,297162,297163,297168,297169,297170,297171,297175,297176,297177,297178,297179,297180,297181,297182,297199,297200,297209,297211,297215,297218,297219,297224,297225,297227,297228,297229,297260,297264,297268,297281,297282,297283,297284,297285,297286,297287,297288,297289,297290,297291,297292,297293,297296,297308,297316,297341,297351,297355,297359,297406,297411,297424,297425,297426,297429,297430,297431,297432,297433,297434,297435,297462,297467,297468,297469,297474,297480,297483,297484,297485,297486,297487,297488,297494,297495,297496,297497,297498,297499,297501,297502,297503,297504,297505,297537,297552,297557,297558,297559,297560,297562,297563,297597,297598,297599,297603,297604,297605,297606,297618,297620,297653,297656,297657,297658,297659,297660,297661,297662,297663,297664,297665,297666,297669,297670,297671,297672,297673,297674,297675,297678,297722,297723,298404,298464,298525,298530,298549,298608,298628,298629,298631,298632,298641,298644,298653,298671,298674,298678,298679,298681,298694,298698,298700,298710,298712,298713,298724,298728,298733,298738,298743,298744,298747,298753,298754,298755,298756,298759,298760,298762,298767,298768,298770,298771,298778,298779,298781,298782,298783,298787,298800,298807,298809,298810,298811,298812,298816,298831,298835,298850,298853,298854,298855,298906,298991,298996,298997,298998,299000,299005,299038,299042,299061,299062,299064,299065,299067,299096,299149,299178,299180,299183,299184,299185,299316,299317,299318,299324,299325,299326,299327,299329};

  //run C int Runs[nhist] = {299338,299368,299369,299370,299380,299381,299394,299395,299396,299414,299419,299420,299440,299443,299450,299477,299478,299479,299480,299481,299496,299592,299593,299594,299595,299597,299598,299614,299616,299617,299649,299662,299663,299664,299731,299746,299764,299774,299775,299780,299786,299799,299804,299806,299807,299808,299809,299813,299815,299819,299825,299829,299831,299833,299913,299917,299929,299930,299934,299936,299937,299958,299992,299996,300007,300012,300013,300015,300016,300017,300018,300019,300027,300029,300043,300049,300050,300064,300065,300067,300079,300087,300088,300101,300104,300105,300106,300107,300117,300122,300123,300124,300155,300156,300157,300167,300226,300233,300234,300235,300236,300237,300238,300239,300240,300241,300273,300280,300281,300282,300283,300284,300293,300308,300309,300310,300312,300313,300314,300328,300360,300361,300364,300365,300366,300367,300368,300369,300370,300371,300372,300373,300374,300375,300389,300390,300391,300392,300393,300394,300395,300396,300397,300398,300399,300400,300401,300424,300459,300461,300462,300463,300464,300466,300467,300488,300497,300498,300499,300500,300501,300514,300515,300516,300517,300538,300539,300545,300548,300551,300552,300558,300560,300561,300574,300575,300576,300584,300631,300632,300633,300635,300636,300673,300674,300675,300676,300742,300777,300780,300781,300785,300806,300811,300812,300816,300817,300927,300933,300952,300958,300973,300975,301046,301057,301080,301086,301087,301088,301094,301112,301120,301141,301142,301147,301161,301165,301172,301179,301180,301183,301249,301273,301281,301283,301293,301298,301313,301323,301330,301359,301383,301384,301391,301392,301393,301394,301395,301396,301397,301398,301399,301414,301417,301427,301439,301447,301448,301449,301450,301457,301461,301472,301473,301474,301475,301476,301480,301519,301524,301525,301528,301529,301530,301531,301532,301544,301550,301557,301567,301579,301627,301664,301665,301674,301694,301809,301891,301897,301904,301909,301912,301913,301914,301919,301941,301951,301959,301960,301969,301970,301983,301984,301985,301986,301987,301997,301998,302015,302019,302023,302026,302027,302029};

  //run D int Runs[nhist] = {302030,302031,302033,302034,302036,302037,302038,302040,302041,302042,302043,302044,302124,302131,302132,302153,302159,302163,302165,302166,302225,302228,302229,302237,302239,302240,302262,302263,302277,302278,302279,302280,302322,302328,302337,302342,302343,302344,302349,302350,302388,302392,302393,302448,302472,302473,302474,302475,302476,302479,302484,302485,302486,302487,302488,302489,302490,302491,302492,302493,302494,302503,302509,302513,302522,302523,302525,302526,302533,302543,302548,302550,302551,302553,302554,302555,302563,302564,302565,302566,302567,302569,302570,302571,302572,302573,302596,302597,302620,302624,302626,302634,302635,302646,302651,302654,302660,302661,302663,302694,302695,302804,302806,302820,302821,302829,302839,302926,302975,302978,302995};

  //run E int Runs[nhist] = {303569,303572,303573,303574,303575,303576,303595,303601,303676,303728,303729,303808,303813,303816,303817,303818,303819,303824,303825,303832,303838,303885,303948,303989,303998,303999,304000,304013,304062,304119,304120,304125,304144,304149,304153,304158,304169,304170,304185,304189,304190,304196,304197,304198,304199,304200,304204,304209,304254,304291,304292,304326,304332,304333,304350,304354,304364,304366,304435,304446,304447,304448,304449,304451,304452,304453,304505,304506,304507,304508,304562,304616,304625,304626,304654,304655,304661,304662,304663,304671,304672,304711,304722,304737,304738,304739,304740,304775,304776,304777,304778,304784,304789,304795,304796,304797,304821,304822,304826};

  //int Runs[] = {304292};
  //nhist = sizeof(Runs)/sizeof(Run[0]);

  //run G int Runs[nhist] = {306480,306481,306486,306487,306495,306496,306498,306499,306502,306503,306512,306517,306518,306520,306521,306522,306523,306526,306527,306528,306529,306531,306533,306534,306535,306536,306537,306538,306542,306545,306546,306547,306548,306549,306550,306552,306553,306554,306558,306559,306561,306563,306566,306569,306570,306571,306572,306575,306576,306577,306579,306580,306584,306595,306598,306604,306622,306624,306626,306627,306628,306629,306630,306631,306635,306636,306640,306645,306646,306647,306650,306651,306652,306653,306654,306656,306657,306696,306701,306702,306705,306708,306709,306722,306724,306742,306743,306744,306761,306769,306770,306772,306773,306776,306777,306785,306791,306792,306793,306794,306795,306799,306801,306802,306810,306811,306816,306818,306820,306822,306824,306826};

  //int Runs[nhist] = {306832,306836,306838,306889,306896,306897,306915,306918,306926,306929,306933,306934,306936,306952,306954,306955,306961,306964,306981,306982,306984,306987,306988,306989,306996,306997,307001,307003,307013,307014,307015,307016,307017,307039,307040,307041,307042,307044,307045,307046,307047,307048,307049,307050,307051,307052,307053,307054,307055,307062,307063,307072,307073,307075,307076,307081,307082,307188,307214,307215,307216,307242,307248,307252,307258,307259,307265,307266,307268,307269,307270,307271,307272,307318,307320,307321,307322,307325,307327,307331,307333,307335,307341,307349,307350,307351,307352,307383,307390,307399,307412,307417,307421,307450,307452,307456,307495};
}
