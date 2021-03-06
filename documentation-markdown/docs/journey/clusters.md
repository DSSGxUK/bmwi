# Cluster Analysis 
This section talks about the clusters that we have built 
and used for the model. 

## Need for clusters 
We wanted to forecast unemployment rate for all 401 Kreise of Germany. 
Of course, we could have create 401 independent time series models, one for each Kreis. 
However, this would mean that all models won't learn from the unemployment rate time series of other Kreise. 
We believed that some Kreise must be similar to each other, 
and can benefit from incorporating each other's data in the forecasting process.

We used unsupervised classification methods to divide Kreise into clusters, 
based on 176 structural features collected during 2017-2018 for each Kreise. 
These clusters were later used in hierarchical time series models, and in VAR models.  


## Type of Clusters 
We explored 4 different methods to cluster the Kreise

### Bundesland

Each Kreise belongs to one out for 16 Bundeslands. 
Kreise that belong to the same Bundesland have a similar geographic location, 
and are also affected by the same decisions that are made on a Bundesland level. 

![Bundesland](./clusters_screenshots/bundesland.png)
<!-- ![Bundesland](https://i.imgur.com/Se78LkN.png) -->


### PCA & K-means

We started with clustering using 169 numerical features (disregarding the 7 categorical features). 

First, we reduced the features dimension using PCA 
with 3 components. 

1. The first component explained 53.0% of the variance of the features, 
and represented mainly the population size features. 
2. The second component explained 11.4% of the variance of the features, 
and represented mainly the rural vs. city features. 
3. The third component explained 4.7% of the variance of the features, 
and represented mainly the economical features. 

![PCA & K-means](./clusters_screenshots/PCA1.png)

![PCA & K-means](./clusters_screenshots/PCA2.png)

Then, we used K-means to cluster the Kreise into 3 clusters based on the PCA features. 

![PCA & K-means](./clusters_screenshots/Kmeans_of_PCA.png)

![PCA & K-means](./clusters_screenshots/hierarchy_PCA.png)


### tSNE

We started with clustering using 169 numerical features (disregarding the 7 categorical features). 

First, we reduced the features dimension using tSNE with 3 components. 

![PCA & K-means](./clusters_screenshots/tSNE.png)

Then, we used K-means to cluster the Kreise into 3 clusters based on the PCA features. 

![PCA & K-means](./clusters_screenshots/Kmeans_of_tSNE.png)


### K-modes

To incorporate categorical features as well, we also tried K-modes classification on the original 176 features, both numerical and categorical. 


## Cluster groups 

<details>
  <summary> <strong> Bundesland </strong> </summary>
  <ul>
    <li>
    <strong>Baden-W??rttemberg: </strong> Stuttgart, B??blingen, Esslingen, G??ppingen, Ludwigsburg, Rems-Murr-Kreis, Heilbronn, Heilbronn, Hohenlohekreis, Schw??bisch Hall, Main-Tauber-Kreis, Heidenheim, Ostalbkreis, Baden-Baden, Karlsruhe, Karlsruhe, Rastatt, Heidelberg, Mannheim, Neckar-Odenwald-Kreis, Rhein-Neckar-Kreis, Pforzheim, Calw, Enzkreis, Freudenstadt, Freiburg im Breisgau, Breisgau-Hochschwarzwald, Emmendingen, Ortenaukreis, Rottweil, Schwarzwald-Baar-Kreis, Tuttlingen, Konstanz, L??rrach, Waldshut, Reutlingen, T??bingen, Zollernalbkreis, Ulm, Alb-Donau-Kreis, Biberach, Bodenseekreis, Ravensburg, Sigmaringen </li>
    <li>
    <strong>Berlin: </strong> Berlin </li>
    <li>
    <strong>Brandenburg: </strong> Brandenburg an der Havel, Cottbus, Frankfurt (Oder), Potsdam, Barnim, Dahme-Spreewald, Elbe-Elster, Havelland, M??rkisch-Oderland, Oberhavel, Oberspreewald-Lausitz, Oder-Spree, Ostprignitz-Ruppin, Potsdam-Mittelmark, Prignitz, Spree-Nei??e, Teltow-Fl??ming, Uckermark </li>
    <li>
    <strong>Bremen: </strong> Bremen, Bremerhaven </li>
    <li>
    <strong>Freistaat Bayern: </strong> Ingolstadt, M??nchen, Rosenheim, Alt??tting, Berchtesgadener Land, Bad T??lz-Wolfratshausen, Dachau, Ebersberg, Eichst??tt, Erding, Freising, F??rstenfeldbruck, Garmisch-Partenkirchen, Landsberg am Lech, Miesbach, M??hldorf a.Inn, M??nchen, Neuburg-Schrobenhausen, Pfaffenhofen a.d.Ilm, Rosenheim, Starnberg, Traunstein, Weilheim-Schongau, Landshut, Passau, Straubing, Deggendorf, Freyung-Grafenau, Kelheim, Landshut, Passau, Regen, Rottal-Inn, Straubing-Bogen, Dingolfing-Landau, Amberg, Regensburg, Weiden i.d.OPf., Amberg-Sulzbach, Cham, Neumarkt i.d.OPf., Neustadt a.d.Waldnaab, Regensburg, Schwandorf, Tirschenreuth, Bamberg, Bayreuth, Coburg, Hof, Bamberg, Bayreuth, Coburg, Forchheim, Hof, Kronach, Kulmbach, Lichtenfels, Wunsiedel i.Fichtelgebirge, Ansbach, Erlangen, F??rth, N??rnberg, Schwabach, Ansbach, Erlangen-H??chstadt, F??rth, N??rnberger Land, Neustadt a.d.Aisch-Bad Windsheim, Roth, Wei??enburg-Gunzenhausen, Aschaffenburg, Schweinfurt, W??rzburg, Aschaffenburg, Bad Kissingen, Rh??n-Grabfeld, Ha??berge, Kitzingen, Miltenberg, Main-Spessart, Schweinfurt, W??rzburg, Augsburg, Kaufbeuren, Kempten (Allg??u), Memmingen, Aichach-Friedberg, Augsburg, Dillingen a.d.Donau, G??nzburg, Neu-Ulm, Lindau (Bodensee), Ostallg??u, Unterallg??u, Donau-Ries, Oberallg??u </li>
    <li>
    <strong>Hamburg: </strong> Hamburg </li>
    <li>
    <strong>Hessen: </strong> Kreisfreie Stadt Darmstadt, Kreisfreie Stadt Frankfurt am Main, Kreisfreie Stadt Offenbach am Main, Landeshauptstadt Wiesbaden, Bergstra??e, Darmstadt-Dieburg, Gro??-Gerau, Hochtaunus, Main-Kinzig, Main-Taunus, Odenwaldkreis, Offenbach, Rheingau-Taunus, Wetterau, Gie??en, Lahn-Dill, Limburg-Weilburg, Marburg-Biedenkopf, Vogelsberg, Kreisfreie Stadt Kassel, Fulda, Hersfeld-Rotenburg, Kassel, Schwalm-Eder, Waldeck-Frankenberg, Werra-Mei??ner </li>        
    <li>
    <strong>Mecklenburg-Vorpommern: </strong> Rostock, Hansestadt, Schwerin, Landeshauptstadt, Mecklenburgische Seenplatte, Landkreis Rostock, Vorpommern-R??gen, Nordwestmecklenburg, Vorpommern-Greifswald, Ludwigslust-Parchim </li>
    <li>
    <strong>Niedersachsen: </strong> Braunschweig, Salzgitter, Wolfsburg, Gifhorn, Goslar, Helmstedt, Northeim, Peine, Wolfenb??ttel, G??ttingen, Hannover, Diepholz, Hameln-Pyrmont, Hildesheim, Holzminden, Nienburg/Weser, Schaumburg, Celle, Cuxhaven, Harburg, L??chow-Dannenberg, L??neburg, Osterholz, Rotenburg (W??mme), Heidekreis, Stade, Uelzen, Verden, Delmenhorst, Emden, Oldenburg, Osnabr??ck, Wilhelmshaven, Ammerland, Aurich, Cloppenburg, Emsland, Friesland, Grafschaft Bentheim, Leer, Oldenburg, Osnabr??ck, Vechta, Wesermarsch, Wittmund </li>
    <li>
    <strong>Nordrhein-Westfalen: </strong> D??sseldorf, Duisburg, Essen, Krefeld, M??nchengladbach, M??lheim an der Ruhr, Oberhausen, Remscheid, Solingen, Wuppertal, Kleve, Mettmann, Rhein-Kreis Neuss, Viersen, Wesel, Bonn, K??ln, Leverkusen, Aachen, D??ren, Rhein-Erft-Kreis, Euskirchen, Heinsberg, Oberbergischer Kreis, Rheinisch-Bergischer Kreis, Rhein-Sieg-Kreis, Bottrop, Gelsenkirchen, M??nster, Borken, Coesfeld, Recklinghausen, Steinfurt, Warendorf, Bielefeld, G??tersloh, Herford, H??xter, Lippe, Minden-L??bbecke, Paderborn, Bochum, Dortmund, Hagen, Hamm, Herne, Ennepe-Ruhr-Kreis, Hochsauerlandkreis, M??rkischer Kreis, Olpe, Siegen-Wittgenstein, Soest, Unna </li>
    <li>
    <strong>Rheinland-Pfalz: </strong> Stadt Koblenz, Ahrweiler, Altenkirchen (Ww), Bad Kreuznach, Birkenfeld, Cochem-Zell, Mayen-Koblenz, Neuwied, Rhein-Hunsr??ck-Kreis, Rhein-Lahn-Kreis, Westerwaldkreis, Stadt Trier, Bernkastel-Wittlich, Eifelkreis Bitburg-Pr??m, Vulkaneifel, Trier-Saarburg, Stadt Frankenthal (Pfalz), Stadt Kaiserslautern, Stadt Landau in der Pfalz, Stadt Ludwigshafen a. Rh., Stadt Mainz, Stadt Neustadt a.d. W., Stadt Pirmasens, Stadt Speyer, Stadt Worms, Stadt Zweibr??cken, Alzey-Worms, Bad D??rkheim, Donnersbergkreis, Germersheim, Kaiserslautern, Kusel, S??dliche Weinstra??e, Rhein-Pfalz-Kreis, Mainz-Bingen, S??dwestpfalz </li>
    <li>
    <strong>Saarland: </strong> Regionalverband Saarbr??cken, Landkreis Merzig-Wadern, Landkreis Neunkirchen, Landkreis Saarlouis, Saarpfalz-Kreis, Landkreis St. Wendel </li>
    <li>
    <strong>Sachsen: </strong> Chemnitz, Erzgebirgskreis, Mittelsachsen, Vogtlandkreis, Zwickau, Dresden, Bautzen, G??rlitz, Mei??en, S??chsische Schweiz-Osterzgebirge, Leipzig, Leipzig, Nordsachsen </li>
    <li>
    <strong>Sachsen-Anhalt: </strong> Dessau-Ro??lau, Halle (Saale), Magdeburg, Altmarkkreis Salzwedel, Anhalt-Bitterfeld, B??rde, Burgenlandkreis, Harz, Jerichower Land, Mansfeld-S??dharz, Saalekreis, Salzlandkreis, Stendal, Wittenberg </li>
    <li>
    <strong>Schleswig-Holstein : </strong> Flensburg, Stadt, Kiel, Landeshauptstadt, L??beck, Hansestadt, Neum??nster, Stadt, Dithmarschen, Herzogtum Lauenburg, Nordfriesland, Ostholstein, Pinneberg, Pl??n, Rendsburg-Eckernf??rde, Schleswig-Flensburg, Segeberg, Steinburg, Stormarn </li>
    <li>
    <strong>Th??ringen: </strong> Erfurt, Gera, Jena, Suhl, Weimar, Eisenach, Eichsfeld, Nordhausen, Wartburgkreis, Unstrut-Hainich-Kreis, Kyffh??userkreis, Schmalkalden-Meiningen, Gotha, S??mmerda, Hildburghausen, Ilm-Kreis, Weimarer Land, Sonneberg, Saalfeld-Rudolstadt, Saale-Holzland-Kreis, Saale-Orla-Kreis, Greiz, Altenburger Land </li>

  </ul>
</details>

<details>
  <summary> <strong> PCA & K-means </strong> </summary>
  <ul>
    <li>
    <strong>Cluster 1: </strong> Flensburg, Stadt, Neum??nster, Stadt, Dithmarschen, Herzogtum Lauenburg, Nordfriesland, Ostholstein, Pinneberg, Pl??n, Rendsburg-Eckernf??rde, Schleswig-Flensburg, Segeberg, Steinburg, Stormarn, Salzgitter, Wolfsburg, Gifhorn, Goslar, Helmstedt, Northeim, Peine, Wolfenb??ttel, G??ttingen, Diepholz, Hameln-Pyrmont, Hildesheim, Holzminden, Nienburg/Weser, Schaumburg, Celle, Cuxhaven, Harburg, L??chow-Dannenberg, L??neburg, Osterholz, Rotenburg (W??mme), Heidekreis, Stade, Uelzen, Verden, Delmenhorst, Emden, Oldenburg, Stadt, Osnabr??ck, Stadt, Wilhelmshaven, Ammerland, Aurich, Cloppenburg, Emsland, Friesland, Grafschaft Bentheim, Leer, Oldenburg, Kreis, Osnabr??ck, Kreis, Vechta, Wesermarsch, Wittmund, Bremerhaven, M??lheim an der Ruhr, Remscheid, Solingen, Kleve, Viersen, Leverkusen, D??ren, Euskirchen, Heinsberg, Oberbergischer Kreis, Rheinisch-Bergischer Kreis, Bottrop, Coesfeld, Warendorf, Herford, H??xter, Lippe, Minden-L??bbecke, Paderborn, Hagen, Hamm, Hochsauerlandkreis, Olpe, Siegen-Wittgenstein, Soest, Bergstra??e, Darmstadt-Dieburg, Hochtaunus, Main-Taunus, Odenwaldkreis, Rheingau-Taunus, Wetterau, Gie??en, Lahn-Dill, Limburg-Weilburg, Marburg-Biedenkopf, Vogelsberg, Fulda, Hersfeld-Rotenburg, Kassel, Schwalm-Eder, Waldeck-Frankenberg, Werra-Mei??ner, Stadt Koblenz, Ahrweiler, Altenkirchen (Ww), Bad Kreuznach, Birkenfeld, Cochem-Zell, Mayen-Koblenz, Neuwied, Rhein-Hunsr??ck-Kreis, Rhein-Lahn-Kreis, Westerwaldkreis, Stadt Trier, Bernkastel-Wittlich, Eifelkreis Bitburg-Pr??m, Vulkaneifel, Trier-Saarburg, Stadt Frankenthal (Pfalz), Stadt Kaiserslautern, Stadt Landau in der Pfalz, Stadt Neustadt a.d. W., Stadt Pirmasens, Stadt Speyer, Stadt Worms, Stadt Zweibr??cken, Alzey-Worms, Bad D??rkheim, Donnersbergkreis, Germersheim, Kaiserslautern, Kusel, S??dliche Weinstra??e, Rhein-Pfalz-Kreis, Mainz-Bingen, S??dwestpfalz, G??ppingen, Heilbronn, Stadt, Heilbronn, Kreis, Hohenlohekreis, Schw??bisch Hall, Main-Tauber-Kreis, Heidenheim, Ostalbkreis, Baden-Baden, Rastatt, Neckar-Odenwald-Kreis, Pforzheim, Calw, Enzkreis, Freudenstadt, Breisgau-Hochschwarzwald, Emmendingen, Rottweil, Schwarzwald-Baar-Kreis, Tuttlingen, Konstanz, L??rrach, Waldshut, Reutlingen, T??bingen, Zollernalbkreis, Ulm, Alb-Donau-Kreis, Biberach, Bodenseekreis, Ravensburg, Sigmaringen, Ingolstadt, Alt??tting, Berchtesgadener Land, Bad T??lz-Wolfratshausen, Dachau, Ebersberg, Eichst??tt, Erding, Freising, F??rstenfeldbruck, Garmisch-Partenkirchen, Landsberg am Lech, Miesbach, M??hldorf a.Inn, Neuburg-Schrobenhausen, Pfaffenhofen a.d.Ilm, Rosenheim, Kreis, Starnberg, Traunstein, Weilheim-Schongau, Landshut, Stadt, Passau, Stadt, Straubing, Deggendorf, Freyung-Grafenau, Kelheim, Landshut, Kreis, Passau, Kreis, Regen, Rottal-Inn, Straubing-Bogen, Dingolfing-Landau, Amberg, Weiden i.d.OPf., Amberg-Sulzbach, Cham, Neumarkt i.d.OPf., Neustadt a.d.Waldnaab, Regensburg, Kreis, Schwandorf, Tirschenreuth, Bamberg, Stadt, Bayreuth, Stadt, Coburg, Stadt, Hof, Stadt, Bamberg, Kreis, Bayreuth, Kreis, Coburg, Kreis, Forchheim, Hof, Kreis, Kronach, Kulmbach, Lichtenfels, Wunsiedel i.Fichtelgebirge, Ansbach, Stadt, Erlangen, F??rth, Stadt, Schwabach, Ansbach, Kreis, Erlangen-H??chstadt, F??rth, Kreis, N??rnberger Land, Neustadt a.d.Aisch-Bad Windsheim, Roth, Wei??enburg-Gunzenhausen, Aschaffenburg, Stadt, Schweinfurt, Stadt, W??rzburg, Stadt, Aschaffenburg, Kreis, Bad Kissingen, Rh??n-Grabfeld, Ha??berge, Kitzingen, Miltenberg, Main-Spessart, Schweinfurt, Kreis, W??rzburg, Kreis, Kaufbeuren, Kempten (Allg??u), Memmingen, Aichach-Friedberg, Augsburg, Kreis, Dillingen a.d.Donau, G??nzburg, Neu-Ulm, Lindau (Bodensee), Ostallg??u, Unterallg??u, Donau-Ries, Oberallg??u, Landkreis Merzig-Wadern, Landkreis Neunkirchen, Landkreis Saarlouis, Saarpfalz-Kreis, Landkreis St. Wendel, Brandenburg an der Havel, Cottbus, Frankfurt (Oder), Potsdam, Barnim, Dahme-Spreewald, Elbe-Elster, Havelland, M??rkisch-Oderland, Oberhavel, Oberspreewald-Lausitz, Oder-Spree, Ostprignitz-Ruppin, Potsdam-Mittelmark, Prignitz, Spree-Nei??e, Teltow-Fl??ming, Uckermark, Rostock, Hansestadt, Schwerin, Landeshauptstadt, Mecklenburgische Seenplatte, Landkreis Rostock, Vorpommern-R??gen, Nordwestmecklenburg, Vorpommern-Greifswald, Ludwigslust-Parchim, Chemnitz, Erzgebirgskreis, Mittelsachsen, Vogtlandkreis, Zwickau, Bautzen, G??rlitz, Mei??en, S??chsische Schweiz-Osterzgebirge, Leipzig, Kreis, Nordsachsen, Dessau-Ro??lau, Altmarkkreis Salzwedel, Anhalt-Bitterfeld, B??rde, Burgenlandkreis, Harz, Jerichower Land, Mansfeld-S??dharz, Saalekreis, Salzlandkreis, Stendal, Wittenberg, Gera, Jena, Suhl, Weimar, Eisenach, Eichsfeld, Nordhausen, Wartburgkreis, Unstrut-Hainich-Kreis, Kyffh??userkreis, Schmalkalden-Meiningen, Gotha, S??mmerda, Hildburghausen, Ilm-Kreis, Weimarer Land, Sonneberg, Saalfeld-Rudolstadt, Saale-Holzland-Kreis, Saale-Orla-Kreis, Greiz, Altenburger Land </li>
    <li>
    <strong>Cluster 2: </strong> Hamburg, Berlin </li>
    <li>
    <strong>Cluster 3: </strong> Kiel, Landeshauptstadt, L??beck, Hansestadt, Braunschweig, Hannover, Bremen, D??sseldorf, Duisburg, Essen, Krefeld, M??nchengladbach, Oberhausen, Wuppertal, Mettmann, Rhein-Kreis Neuss, Wesel, Bonn, K??ln, Aachen, Rhein-Erft-Kreis, Rhein-Sieg-Kreis, Gelsenkirchen, M??nster, Borken, Recklinghausen, Steinfurt, Bielefeld, G??tersloh, Bochum, Dortmund, Herne, Ennepe-Ruhr-Kreis, M??rkischer Kreis, Unna, Kreisfreie Stadt Darmstadt, Kreisfreie Stadt Frankfurt am Main, Kreisfreie Stadt Offenbach am Main, Landeshauptstadt Wiesbaden, Gro??-Gerau, Main-Kinzig, Offenbach, Kreisfreie Stadt Kassel, Stadt Ludwigshafen a. Rh., Stadt Mainz, Stuttgart, B??blingen, Esslingen, Ludwigsburg, Rems-Murr-Kreis, Karlsruhe, Stadt, Karlsruhe, Kreis, Heidelberg, Mannheim, Rhein-Neckar-Kreis, Freiburg im Breisgau, Ortenaukreis, M??nchen, Landeshauptstadt, Rosenheim, Stadt, M??nchen, Kreis, Regensburg, Stadt, N??rnberg, Augsburg, Stadt, Regionalverband Saarbr??cken, Dresden, Leipzig, Stadt, Halle (Saale), Magdeburg, Erfurt </li>

  </ul>
</details>


<details>
  <summary> <strong> tSNE & K-means </strong> </summary>
  <ul>
    <li>
    <strong>Cluster 1: </strong> Dithmarschen, Herzogtum Lauenburg, Nordfriesland, Ostholstein, Pl??n, Schleswig-Flensburg, Steinburg, Goslar, Helmstedt, Northeim, Peine, Wolfenb??ttel, Hameln-Pyrmont, Holzminden, Schaumburg, Celle, L??chow-Dannenberg, L??neburg, Osterholz, Heidekreis, Uelzen, Ammerland, Aurich, Friesland, Leer, Wesermarsch, Wittmund, Bottrop, H??xter, Odenwaldkreis, Vogelsberg, Hersfeld-Rotenburg, Schwalm-Eder, Waldeck-Frankenberg, Werra-Mei??ner, Ahrweiler, Altenkirchen (Ww), Bad Kreuznach, Birkenfeld, Cochem-Zell, Rhein-Hunsr??ck-Kreis, Rhein-Lahn-Kreis, Bernkastel-Wittlich, Eifelkreis Bitburg-Pr??m, Vulkaneifel, Trier-Saarburg, Stadt Zweibr??cken, Bad D??rkheim, Donnersbergkreis, Kaiserslautern, Kusel, S??dliche Weinstra??e, S??dwestpfalz, Hohenlohekreis, Schw??bisch Hall, Main-Tauber-Kreis, Neckar-Odenwald-Kreis, Freudenstadt, Sigmaringen, Alt??tting, Berchtesgadener Land, Bad T??lz-Wolfratshausen, Eichst??tt, Erding, Garmisch-Partenkirchen, Landsberg am Lech, Miesbach, M??hldorf a.Inn, Neuburg-Schrobenhausen, Pfaffenhofen a.d.Ilm, Traunstein, Deggendorf, Freyung-Grafenau, Kelheim, Landshut, Kreis, Passau, Kreis, Regen, Rottal-Inn, Straubing-Bogen, Dingolfing-Landau, Amberg-Sulzbach, Cham, Neumarkt i.d.OPf., Neustadt a.d.Waldnaab, Regensburg, Kreis, Schwandorf, Tirschenreuth, Bamberg, Kreis, Bayreuth, Kreis, Coburg, Kreis, Forchheim, Hof, Kreis, Kronach, Kulmbach, Lichtenfels, Wunsiedel i.Fichtelgebirge, Ansbach, Kreis, Neustadt a.d.Aisch-Bad Windsheim, Roth, Wei??enburg-Gunzenhausen, Bad Kissingen, Rh??n-Grabfeld, Ha??berge, Kitzingen, Main-Spessart, Schweinfurt, Kreis, Aichach-Friedberg, Dillingen a.d.Donau, G??nzburg, Ostallg??u, Unterallg??u, Donau-Ries, Oberallg??u, Landkreis Merzig-Wadern, Landkreis Neunkirchen, Landkreis Saarlouis, Saarpfalz-Kreis, Landkreis St. Wendel, Cottbus, Barnim, Dahme-Spreewald, Elbe-Elster, Havelland, M??rkisch-Oderland, Oberhavel, Oberspreewald-Lausitz, Oder-Spree, Ostprignitz-Ruppin, Potsdam-Mittelmark, Prignitz, Spree-Nei??e, Teltow-Fl??ming, Uckermark, Rostock, Hansestadt, Mecklenburgische Seenplatte, Landkreis Rostock, Vorpommern-R??gen, Nordwestmecklenburg, Vorpommern-Greifswald, Ludwigslust-Parchim, Chemnitz, Erzgebirgskreis, Mittelsachsen, Vogtlandkreis, Zwickau, Bautzen, G??rlitz, Mei??en, S??chsische Schweiz-Osterzgebirge, Leipzig, Kreis, Nordsachsen, Altmarkkreis Salzwedel, Anhalt-Bitterfeld, B??rde, Burgenlandkreis, Harz, Jerichower Land, Mansfeld-S??dharz, Saalekreis, Salzlandkreis, Stendal, Wittenberg, Eichsfeld, Nordhausen, Wartburgkreis, Unstrut-Hainich-Kreis, Kyffh??userkreis, Schmalkalden-Meiningen, Gotha, S??mmerda, Hildburghausen, Ilm-Kreis, Weimarer Land, Sonneberg, Saalfeld-Rudolstadt, Saale-Holzland-Kreis, Saale-Orla-Kreis, Greiz, Altenburger Land</li>
    <li>
    <strong>Cluster 2: </strong> Pinneberg, Rendsburg-Eckernf??rde, Segeberg, Stormarn, Hamburg, Gifhorn, G??ttingen, Hannover, Diepholz, Hildesheim, Nienburg/Weser, Cuxhaven, Harburg, Rotenburg (W??mme), Stade, Verden, Cloppenburg, Emsland, Grafschaft Bentheim, Oldenburg, Kreis, Osnabr??ck, Kreis, Vechta, Kleve, Mettmann, Rhein-Kreis Neuss, Viersen, Wesel, K??ln, Aachen, D??ren, Rhein-Erft-Kreis, Euskirchen, Heinsberg, Oberbergischer Kreis, Rheinisch-Bergischer Kreis, Rhein-Sieg-Kreis, Borken, Coesfeld, Recklinghausen, Steinfurt, Warendorf, G??tersloh, Herford, Lippe, Minden-L??bbecke, Paderborn, Ennepe-Ruhr-Kreis, Hochsauerlandkreis, M??rkischer Kreis, Olpe, Siegen-Wittgenstein, Soest, Unna, Kreisfreie Stadt Frankfurt am Main, Kreisfreie Stadt Offenbach am Main, Bergstra??e, Darmstadt-Dieburg, Gro??-Gerau, Hochtaunus, Main-Kinzig, Main-Taunus, Offenbach, Rheingau-Taunus, Wetterau, Gie??en, Lahn-Dill, Limburg-Weilburg, Marburg-Biedenkopf, Fulda, Kassel, Mayen-Koblenz, Neuwied, Westerwaldkreis, Alzey-Worms, Germersheim, Rhein-Pfalz-Kreis, Mainz-Bingen, Stuttgart, B??blingen, Esslingen, G??ppingen, Ludwigsburg, Rems-Murr-Kreis, Heilbronn, Kreis, Heidenheim, Ostalbkreis, Baden-Baden, Karlsruhe, Kreis, Rastatt, Rhein-Neckar-Kreis, Pforzheim, Calw, Enzkreis, Breisgau-Hochschwarzwald, Emmendingen, Ortenaukreis, Rottweil, Schwarzwald-Baar-Kreis, Tuttlingen, Konstanz, L??rrach, Waldshut, Reutlingen, T??bingen, Zollernalbkreis, Alb-Donau-Kreis, Biberach, Bodenseekreis, Ravensburg, M??nchen, Landeshauptstadt, Rosenheim, Stadt, Dachau, Ebersberg, Freising, F??rstenfeldbruck, M??nchen, Kreis, Rosenheim, Kreis, Starnberg, Weilheim-Schongau, Erlangen-H??chstadt, F??rth, Kreis, N??rnberger Land, Aschaffenburg, Kreis, Miltenberg, W??rzburg, Kreis, Augsburg, Kreis, Neu-Ulm, Regionalverband Saarbr??cken, Berlin</li>
    <li>
    <strong>Cluster 3: </strong> Flensburg, Stadt, Kiel, Landeshauptstadt, L??beck, Hansestadt, Neum??nster, Stadt, Braunschweig, Salzgitter, Wolfsburg, Delmenhorst, Emden, Oldenburg, Stadt, Osnabr??ck, Stadt, Wilhelmshaven, Bremen, Bremerhaven, D??sseldorf, Duisburg, Essen, Krefeld, M??nchengladbach, M??lheim an der Ruhr, Oberhausen, Remscheid, Solingen, Wuppertal, Bonn, Leverkusen, Gelsenkirchen, M??nster, Bielefeld, Bochum, Dortmund, Hagen, Hamm, Herne, Kreisfreie Stadt Darmstadt, Landeshauptstadt Wiesbaden, Kreisfreie Stadt Kassel, Stadt Koblenz, Stadt Trier, Stadt Frankenthal (Pfalz), Stadt Kaiserslautern, Stadt Landau in der Pfalz, Stadt Ludwigshafen a. Rh., Stadt Mainz, Stadt Neustadt a.d. W., Stadt Pirmasens, Stadt Speyer, Stadt Worms, Heilbronn, Stadt, Karlsruhe, Stadt, Heidelberg, Mannheim, Freiburg im Breisgau, Ulm, Ingolstadt, Landshut, Stadt, Passau, Stadt, Straubing, Amberg, Regensburg, Stadt, Weiden i.d.OPf., Bamberg, Stadt, Bayreuth, Stadt, Coburg, Stadt, Hof, Stadt, Ansbach, Stadt, Erlangen, F??rth, Stadt, N??rnberg, Schwabach, Aschaffenburg, Stadt, Schweinfurt, Stadt, W??rzburg, Stadt, Augsburg, Stadt, Kaufbeuren, Kempten (Allg??u), Memmingen, Lindau (Bodensee), Brandenburg an der Havel, Frankfurt (Oder), Potsdam, Schwerin, Landeshauptstadt, Dresden, Leipzig, Stadt, Dessau-Ro??lau, Halle (Saale), Magdeburg, Erfurt, Gera, Jena, Suhl, Weimar, Eisenach</li>    
  </ul>
</details>

<details>
  <summary> <strong> K-modes</strong> </summary>
  <ul>
    <li>
    <strong>Cluster 1: </strong> Neum??nster, Stadt, Herzogtum Lauenburg, Ostholstein, Rendsburg-Eckernf??rde, Schleswig-Flensburg, Segeberg, Wolfenb??ttel, Hameln-Pyrmont, Nienburg/Weser, Celle, Cuxhaven, Rotenburg (W??mme), Stade, Verden, Delmenhorst, Emden, Wilhelmshaven, Aurich, Cloppenburg, Emsland, Grafschaft Bentheim, Leer, Vechta, Warendorf, H??xter, Hochsauerlandkreis, Olpe, Marburg-Biedenkopf, Fulda, Hersfeld-Rotenburg, Schwalm-Eder, Stadt Koblenz, Ahrweiler, Bad Kreuznach, Rhein-Hunsr??ck-Kreis, Bernkastel-Wittlich, Eifelkreis Bitburg-Pr??m, Trier-Saarburg, Donnersbergkreis, Kusel, S??dwestpfalz, Hohenlohekreis, Schw??bisch Hall, Main-Tauber-Kreis, Neckar-Odenwald-Kreis, Freudenstadt, Waldshut, Alb-Donau-Kreis, Biberach, Sigmaringen, Ingolstadt, Alt??tting, Berchtesgadener Land, Bad T??lz-Wolfratshausen, Eichst??tt, Erding, Garmisch-Partenkirchen, Landsberg am Lech, Miesbach, M??hldorf a.Inn, Neuburg-Schrobenhausen, Pfaffenhofen a.d.Ilm, Rosenheim, Kreis, Traunstein, Weilheim-Schongau, Landshut, Stadt, Passau, Stadt, Straubing, Deggendorf, Kelheim, Landshut, Kreis, Passau, Kreis, Regen, Rottal-Inn, Straubing-Bogen, Dingolfing-Landau, Neumarkt i.d.OPf., Regensburg, Kreis, Schwandorf, Bamberg, Stadt, Bayreuth, Stadt, Coburg, Stadt, Hof, Stadt, Bamberg, Kreis, Bayreuth, Kreis, Coburg, Kreis, Forchheim, Hof, Kreis, Kronach, Lichtenfels, Ansbach, Stadt, Ansbach, Kreis, Roth, Wei??enburg-Gunzenhausen, Schweinfurt, Stadt, Rh??n-Grabfeld, Kitzingen, Miltenberg, Main-Spessart, Schweinfurt, Kreis, Kempten (Allg??u), Memmingen, Aichach-Friedberg, Dillingen a.d.Donau, G??nzburg, Ostallg??u, Unterallg??u, Donau-Ries, Brandenburg an der Havel, Cottbus, Nordwestmecklenburg, Anhalt-Bitterfeld, Burgenlandkreis, Altenburger Land</li>
    <li>
    <strong>Cluster 2: </strong> Flensburg, Stadt, Dithmarschen, Nordfriesland, Pl??n, Steinburg, Gifhorn, Goslar, Helmstedt, Northeim, Holzminden, L??chow-Dannenberg, L??neburg, Heidekreis, Uelzen, Wesermarsch, Wittmund, Vogelsberg, Waldeck-Frankenberg, Werra-Mei??ner, Birkenfeld, Cochem-Zell, Vulkaneifel, Freyung-Grafenau, Amberg, Weiden i.d.OPf., Amberg-Sulzbach, Cham, Neustadt a.d.Waldnaab, Tirschenreuth, Kulmbach, Wunsiedel i.Fichtelgebirge, Neustadt a.d.Aisch-Bad Windsheim, Bad Kissingen, Ha??berge, Kaufbeuren, Oberallg??u, Frankfurt (Oder), Potsdam, Barnim, Dahme-Spreewald, Elbe-Elster, Havelland, M??rkisch-Oderland, Oberhavel, Oberspreewald-Lausitz, Oder-Spree, Ostprignitz-Ruppin, Potsdam-Mittelmark, Prignitz, Spree-Nei??e, Teltow-Fl??ming, Uckermark, Schwerin, Landeshauptstadt, Mecklenburgische Seenplatte, Landkreis Rostock, Vorpommern-R??gen, Vorpommern-Greifswald, Ludwigslust-Parchim, Erzgebirgskreis, Mittelsachsen, Vogtlandkreis, Zwickau, Bautzen, G??rlitz, Mei??en, S??chsische Schweiz-Osterzgebirge, Nordsachsen, Dessau-Ro??lau, Magdeburg, Altmarkkreis Salzwedel, B??rde, Harz, Jerichower Land, Mansfeld-S??dharz, Saalekreis, Salzlandkreis, Stendal, Wittenberg, Erfurt, Gera, Suhl, Eisenach, Eichsfeld, Nordhausen, Wartburgkreis, Unstrut-Hainich-Kreis, Kyffh??userkreis, Schmalkalden-Meiningen, Gotha, S??mmerda, Hildburghausen, Ilm-Kreis, Sonneberg, Saalfeld-Rudolstadt, Saale-Holzland-Kreis, Saale-Orla-Kreis, Greiz</li>
    <li>
    <strong>Cluster 3: </strong> Kiel, Landeshauptstadt, L??beck, Hansestadt, Pinneberg, Stormarn, Hamburg, Braunschweig, Salzgitter, Wolfsburg, Peine, G??ttingen, Hannover, Diepholz, Hildesheim, Schaumburg, Harburg, Osterholz, Oldenburg, Stadt, Osnabr??ck, Stadt, Ammerland, Friesland, Oldenburg, Kreis, Osnabr??ck, Kreis, Bremen, Bremerhaven, D??sseldorf, Duisburg, Essen, Krefeld, M??nchengladbach, M??lheim an der Ruhr, Oberhausen, Remscheid, Solingen, Wuppertal, Kleve, Mettmann, Rhein-Kreis Neuss, Viersen, Wesel, Bonn, K??ln, Leverkusen, Aachen, D??ren, Rhein-Erft-Kreis, Euskirchen, Heinsberg, Oberbergischer Kreis, Rheinisch-Bergischer Kreis, Rhein-Sieg-Kreis, Bottrop, Gelsenkirchen, M??nster, Borken, Coesfeld, Recklinghausen, Steinfurt, Bielefeld, G??tersloh, Herford, Lippe, Minden-L??bbecke, Paderborn, Bochum, Dortmund, Hagen, Hamm, Herne, Ennepe-Ruhr-Kreis, M??rkischer Kreis, Siegen-Wittgenstein, Soest, Unna, Kreisfreie Stadt Darmstadt, Kreisfreie Stadt Frankfurt am Main, Kreisfreie Stadt Offenbach am Main, Landeshauptstadt Wiesbaden, Bergstra??e, Darmstadt-Dieburg, Gro??-Gerau, Hochtaunus, Main-Kinzig, Main-Taunus, Odenwaldkreis, Offenbach, Rheingau-Taunus, Wetterau, Gie??en, Lahn-Dill, Limburg-Weilburg, Kreisfreie Stadt Kassel, Kassel, Altenkirchen (Ww), Mayen-Koblenz, Neuwied, Rhein-Lahn-Kreis, Westerwaldkreis, Stadt Trier, Stadt Frankenthal (Pfalz), Stadt Kaiserslautern, Stadt Landau in der Pfalz, Stadt Ludwigshafen a. Rh., Stadt Mainz, Stadt Neustadt a.d. W., Stadt Pirmasens, Stadt Speyer, Stadt Worms, Stadt Zweibr??cken, Alzey-Worms, Bad D??rkheim, Germersheim, Kaiserslautern, S??dliche Weinstra??e, Rhein-Pfalz-Kreis, Mainz-Bingen, Stuttgart, B??blingen, Esslingen, G??ppingen, Ludwigsburg, Rems-Murr-Kreis, Heilbronn, Stadt, Heilbronn, Kreis, Heidenheim, Ostalbkreis, Baden-Baden, Karlsruhe, Stadt, Karlsruhe, Kreis, Rastatt, Heidelberg, Mannheim, Rhein-Neckar-Kreis, Pforzheim, Calw, Enzkreis, Freiburg im Breisgau, Breisgau-Hochschwarzwald, Emmendingen, Ortenaukreis, Rottweil, Schwarzwald-Baar-Kreis, Tuttlingen, Konstanz, L??rrach, Reutlingen, T??bingen, Zollernalbkreis, Ulm, Bodenseekreis, Ravensburg, M??nchen, Landeshauptstadt, Rosenheim, Stadt, Dachau, Ebersberg, Freising, F??rstenfeldbruck, M??nchen, Kreis, Starnberg, Regensburg, Stadt, Erlangen, F??rth, Stadt, N??rnberg, Schwabach, Erlangen-H??chstadt, F??rth, Kreis, N??rnberger Land, Aschaffenburg, Stadt, W??rzburg, Stadt, Aschaffenburg, Kreis, W??rzburg, Kreis, Augsburg, Stadt, Augsburg, Kreis, Neu-Ulm, Lindau (Bodensee), Regionalverband Saarbr??cken, Landkreis Merzig-Wadern, Landkreis Neunkirchen, Landkreis Saarlouis, Saarpfalz-Kreis, Landkreis St. Wendel, Berlin, Rostock, Hansestadt, Chemnitz, Dresden, Leipzig, Stadt, Leipzig, Kreis, Halle (Saale), Jena, Weimar, Weimarer Land</li>
    
  </ul>
</details>