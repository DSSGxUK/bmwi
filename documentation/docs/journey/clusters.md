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
    <strong>Baden-Württemberg: </strong> Stuttgart, Böblingen, Esslingen, Göppingen, Ludwigsburg, Rems-Murr-Kreis, Heilbronn, Heilbronn, Hohenlohekreis, Schwäbisch Hall, Main-Tauber-Kreis, Heidenheim, Ostalbkreis, Baden-Baden, Karlsruhe, Karlsruhe, Rastatt, Heidelberg, Mannheim, Neckar-Odenwald-Kreis, Rhein-Neckar-Kreis, Pforzheim, Calw, Enzkreis, Freudenstadt, Freiburg im Breisgau, Breisgau-Hochschwarzwald, Emmendingen, Ortenaukreis, Rottweil, Schwarzwald-Baar-Kreis, Tuttlingen, Konstanz, Lörrach, Waldshut, Reutlingen, Tübingen, Zollernalbkreis, Ulm, Alb-Donau-Kreis, Biberach, Bodenseekreis, Ravensburg, Sigmaringen </li>
    <strong>Berlin: </strong> Berlin </li>
    <strong>Brandenburg: </strong> Brandenburg an der Havel, Cottbus, Frankfurt (Oder), Potsdam, Barnim, Dahme-Spreewald, Elbe-Elster, Havelland, Märkisch-Oderland, Oberhavel, Oberspreewald-Lausitz, Oder-Spree, Ostprignitz-Ruppin, Potsdam-Mittelmark, Prignitz, Spree-Neiße, Teltow-Fläming, Uckermark </li>
    <strong>Bremen: </strong> Bremen, Bremerhaven </li>
    <strong>Freistaat Bayern: </strong> Ingolstadt, München, Rosenheim, Altötting, Berchtesgadener Land, Bad Tölz-Wolfratshausen, Dachau, Ebersberg, Eichstätt, Erding, Freising, Fürstenfeldbruck, Garmisch-Partenkirchen, Landsberg am Lech, Miesbach, Mühldorf a.Inn, München, Neuburg-Schrobenhausen, Pfaffenhofen a.d.Ilm, Rosenheim, Starnberg, Traunstein, Weilheim-Schongau, Landshut, Passau, Straubing, Deggendorf, Freyung-Grafenau, Kelheim, Landshut, Passau, Regen, Rottal-Inn, Straubing-Bogen, Dingolfing-Landau, Amberg, Regensburg, Weiden i.d.OPf., Amberg-Sulzbach, Cham, Neumarkt i.d.OPf., Neustadt a.d.Waldnaab, Regensburg, Schwandorf, Tirschenreuth, Bamberg, Bayreuth, Coburg, Hof, Bamberg, Bayreuth, Coburg, Forchheim, Hof, Kronach, Kulmbach, Lichtenfels, Wunsiedel i.Fichtelgebirge, Ansbach, Erlangen, Fürth, Nürnberg, Schwabach, Ansbach, Erlangen-Höchstadt, Fürth, Nürnberger Land, Neustadt a.d.Aisch-Bad Windsheim, Roth, Weißenburg-Gunzenhausen, Aschaffenburg, Schweinfurt, Würzburg, Aschaffenburg, Bad Kissingen, Rhön-Grabfeld, Haßberge, Kitzingen, Miltenberg, Main-Spessart, Schweinfurt, Würzburg, Augsburg, Kaufbeuren, Kempten (Allgäu), Memmingen, Aichach-Friedberg, Augsburg, Dillingen a.d.Donau, Günzburg, Neu-Ulm, Lindau (Bodensee), Ostallgäu, Unterallgäu, Donau-Ries, Oberallgäu </li>
    <strong>Hamburg: </strong> Hamburg </li>
    <strong>Hessen: </strong> Kreisfreie Stadt Darmstadt, Kreisfreie Stadt Frankfurt am Main, Kreisfreie Stadt Offenbach am Main, Landeshauptstadt Wiesbaden, Bergstraße, Darmstadt-Dieburg, Groß-Gerau, Hochtaunus, Main-Kinzig, Main-Taunus, Odenwaldkreis, Offenbach, Rheingau-Taunus, Wetterau, Gießen, Lahn-Dill, Limburg-Weilburg, Marburg-Biedenkopf, Vogelsberg, Kreisfreie Stadt Kassel, Fulda, Hersfeld-Rotenburg, Kassel, Schwalm-Eder, Waldeck-Frankenberg, Werra-Meißner </li>        
    <strong>Mecklenburg-Vorpommern: </strong> Rostock, Hansestadt, Schwerin, Landeshauptstadt, Mecklenburgische Seenplatte, Landkreis Rostock, Vorpommern-Rügen, Nordwestmecklenburg, Vorpommern-Greifswald, Ludwigslust-Parchim </li>
    <strong>Niedersachsen: </strong> Braunschweig, Salzgitter, Wolfsburg, Gifhorn, Goslar, Helmstedt, Northeim, Peine, Wolfenbüttel, Göttingen, Hannover, Diepholz, Hameln-Pyrmont, Hildesheim, Holzminden, Nienburg/Weser, Schaumburg, Celle, Cuxhaven, Harburg, Lüchow-Dannenberg, Lüneburg, Osterholz, Rotenburg (Wümme), Heidekreis, Stade, Uelzen, Verden, Delmenhorst, Emden, Oldenburg, Osnabrück, Wilhelmshaven, Ammerland, Aurich, Cloppenburg, Emsland, Friesland, Grafschaft Bentheim, Leer, Oldenburg, Osnabrück, Vechta, Wesermarsch, Wittmund </li>
    <strong>Nordrhein-Westfalen: </strong> Düsseldorf, Duisburg, Essen, Krefeld, Mönchengladbach, Mülheim an der Ruhr, Oberhausen, Remscheid, Solingen, Wuppertal, Kleve, Mettmann, Rhein-Kreis Neuss, Viersen, Wesel, Bonn, Köln, Leverkusen, Aachen, Düren, Rhein-Erft-Kreis, Euskirchen, Heinsberg, Oberbergischer Kreis, Rheinisch-Bergischer Kreis, Rhein-Sieg-Kreis, Bottrop, Gelsenkirchen, Münster, Borken, Coesfeld, Recklinghausen, Steinfurt, Warendorf, Bielefeld, Gütersloh, Herford, Höxter, Lippe, Minden-Lübbecke, Paderborn, Bochum, Dortmund, Hagen, Hamm, Herne, Ennepe-Ruhr-Kreis, Hochsauerlandkreis, Märkischer Kreis, Olpe, Siegen-Wittgenstein, Soest, Unna </li>
    <strong>Rheinland-Pfalz: </strong> Stadt Koblenz, Ahrweiler, Altenkirchen (Ww), Bad Kreuznach, Birkenfeld, Cochem-Zell, Mayen-Koblenz, Neuwied, Rhein-Hunsrück-Kreis, Rhein-Lahn-Kreis, Westerwaldkreis, Stadt Trier, Bernkastel-Wittlich, Eifelkreis Bitburg-Prüm, Vulkaneifel, Trier-Saarburg, Stadt Frankenthal (Pfalz), Stadt Kaiserslautern, Stadt Landau in der Pfalz, Stadt Ludwigshafen a. Rh., Stadt Mainz, Stadt Neustadt a.d. W., Stadt Pirmasens, Stadt Speyer, Stadt Worms, Stadt Zweibrücken, Alzey-Worms, Bad Dürkheim, Donnersbergkreis, Germersheim, Kaiserslautern, Kusel, Südliche Weinstraße, Rhein-Pfalz-Kreis, Mainz-Bingen, Südwestpfalz </li>
    <strong>Saarland: </strong> Regionalverband Saarbrücken, Landkreis Merzig-Wadern, Landkreis Neunkirchen, Landkreis Saarlouis, Saarpfalz-Kreis, Landkreis St. Wendel </li>
    <strong>Sachsen: </strong> Chemnitz, Erzgebirgskreis, Mittelsachsen, Vogtlandkreis, Zwickau, Dresden, Bautzen, Görlitz, Meißen, Sächsische Schweiz-Osterzgebirge, Leipzig, Leipzig, Nordsachsen </li>
    <strong>Sachsen-Anhalt: </strong> Dessau-Roßlau, Halle (Saale), Magdeburg, Altmarkkreis Salzwedel, Anhalt-Bitterfeld, Börde, Burgenlandkreis, Harz, Jerichower Land, Mansfeld-Südharz, Saalekreis, Salzlandkreis, Stendal, Wittenberg </li>
    <strong>Schleswig-Holstein : </strong> Flensburg, Stadt, Kiel, Landeshauptstadt, Lübeck, Hansestadt, Neumünster, Stadt, Dithmarschen, Herzogtum Lauenburg, Nordfriesland, Ostholstein, Pinneberg, Plön, Rendsburg-Eckernförde, Schleswig-Flensburg, Segeberg, Steinburg, Stormarn </li>
    <strong>Thüringen: </strong> Erfurt, Gera, Jena, Suhl, Weimar, Eisenach, Eichsfeld, Nordhausen, Wartburgkreis, Unstrut-Hainich-Kreis, Kyffhäuserkreis, Schmalkalden-Meiningen, Gotha, Sömmerda, Hildburghausen, Ilm-Kreis, Weimarer Land, Sonneberg, Saalfeld-Rudolstadt, Saale-Holzland-Kreis, Saale-Orla-Kreis, Greiz, Altenburger Land </li>

  </ul>
</details>

<details>
  <summary> <strong> PCA & K-means </strong> </summary>
  <ul>
    <li>
    <strong>Cluster 1: </strong> Flensburg, Stadt, Neumünster, Stadt, Dithmarschen, Herzogtum Lauenburg, Nordfriesland, Ostholstein, Pinneberg, Plön, Rendsburg-Eckernförde, Schleswig-Flensburg, Segeberg, Steinburg, Stormarn, Salzgitter, Wolfsburg, Gifhorn, Goslar, Helmstedt, Northeim, Peine, Wolfenbüttel, Göttingen, Diepholz, Hameln-Pyrmont, Hildesheim, Holzminden, Nienburg/Weser, Schaumburg, Celle, Cuxhaven, Harburg, Lüchow-Dannenberg, Lüneburg, Osterholz, Rotenburg (Wümme), Heidekreis, Stade, Uelzen, Verden, Delmenhorst, Emden, Oldenburg, Stadt, Osnabrück, Stadt, Wilhelmshaven, Ammerland, Aurich, Cloppenburg, Emsland, Friesland, Grafschaft Bentheim, Leer, Oldenburg, Kreis, Osnabrück, Kreis, Vechta, Wesermarsch, Wittmund, Bremerhaven, Mülheim an der Ruhr, Remscheid, Solingen, Kleve, Viersen, Leverkusen, Düren, Euskirchen, Heinsberg, Oberbergischer Kreis, Rheinisch-Bergischer Kreis, Bottrop, Coesfeld, Warendorf, Herford, Höxter, Lippe, Minden-Lübbecke, Paderborn, Hagen, Hamm, Hochsauerlandkreis, Olpe, Siegen-Wittgenstein, Soest, Bergstraße, Darmstadt-Dieburg, Hochtaunus, Main-Taunus, Odenwaldkreis, Rheingau-Taunus, Wetterau, Gießen, Lahn-Dill, Limburg-Weilburg, Marburg-Biedenkopf, Vogelsberg, Fulda, Hersfeld-Rotenburg, Kassel, Schwalm-Eder, Waldeck-Frankenberg, Werra-Meißner, Stadt Koblenz, Ahrweiler, Altenkirchen (Ww), Bad Kreuznach, Birkenfeld, Cochem-Zell, Mayen-Koblenz, Neuwied, Rhein-Hunsrück-Kreis, Rhein-Lahn-Kreis, Westerwaldkreis, Stadt Trier, Bernkastel-Wittlich, Eifelkreis Bitburg-Prüm, Vulkaneifel, Trier-Saarburg, Stadt Frankenthal (Pfalz), Stadt Kaiserslautern, Stadt Landau in der Pfalz, Stadt Neustadt a.d. W., Stadt Pirmasens, Stadt Speyer, Stadt Worms, Stadt Zweibrücken, Alzey-Worms, Bad Dürkheim, Donnersbergkreis, Germersheim, Kaiserslautern, Kusel, Südliche Weinstraße, Rhein-Pfalz-Kreis, Mainz-Bingen, Südwestpfalz, Göppingen, Heilbronn, Stadt, Heilbronn, Kreis, Hohenlohekreis, Schwäbisch Hall, Main-Tauber-Kreis, Heidenheim, Ostalbkreis, Baden-Baden, Rastatt, Neckar-Odenwald-Kreis, Pforzheim, Calw, Enzkreis, Freudenstadt, Breisgau-Hochschwarzwald, Emmendingen, Rottweil, Schwarzwald-Baar-Kreis, Tuttlingen, Konstanz, Lörrach, Waldshut, Reutlingen, Tübingen, Zollernalbkreis, Ulm, Alb-Donau-Kreis, Biberach, Bodenseekreis, Ravensburg, Sigmaringen, Ingolstadt, Altötting, Berchtesgadener Land, Bad Tölz-Wolfratshausen, Dachau, Ebersberg, Eichstätt, Erding, Freising, Fürstenfeldbruck, Garmisch-Partenkirchen, Landsberg am Lech, Miesbach, Mühldorf a.Inn, Neuburg-Schrobenhausen, Pfaffenhofen a.d.Ilm, Rosenheim, Kreis, Starnberg, Traunstein, Weilheim-Schongau, Landshut, Stadt, Passau, Stadt, Straubing, Deggendorf, Freyung-Grafenau, Kelheim, Landshut, Kreis, Passau, Kreis, Regen, Rottal-Inn, Straubing-Bogen, Dingolfing-Landau, Amberg, Weiden i.d.OPf., Amberg-Sulzbach, Cham, Neumarkt i.d.OPf., Neustadt a.d.Waldnaab, Regensburg, Kreis, Schwandorf, Tirschenreuth, Bamberg, Stadt, Bayreuth, Stadt, Coburg, Stadt, Hof, Stadt, Bamberg, Kreis, Bayreuth, Kreis, Coburg, Kreis, Forchheim, Hof, Kreis, Kronach, Kulmbach, Lichtenfels, Wunsiedel i.Fichtelgebirge, Ansbach, Stadt, Erlangen, Fürth, Stadt, Schwabach, Ansbach, Kreis, Erlangen-Höchstadt, Fürth, Kreis, Nürnberger Land, Neustadt a.d.Aisch-Bad Windsheim, Roth, Weißenburg-Gunzenhausen, Aschaffenburg, Stadt, Schweinfurt, Stadt, Würzburg, Stadt, Aschaffenburg, Kreis, Bad Kissingen, Rhön-Grabfeld, Haßberge, Kitzingen, Miltenberg, Main-Spessart, Schweinfurt, Kreis, Würzburg, Kreis, Kaufbeuren, Kempten (Allgäu), Memmingen, Aichach-Friedberg, Augsburg, Kreis, Dillingen a.d.Donau, Günzburg, Neu-Ulm, Lindau (Bodensee), Ostallgäu, Unterallgäu, Donau-Ries, Oberallgäu, Landkreis Merzig-Wadern, Landkreis Neunkirchen, Landkreis Saarlouis, Saarpfalz-Kreis, Landkreis St. Wendel, Brandenburg an der Havel, Cottbus, Frankfurt (Oder), Potsdam, Barnim, Dahme-Spreewald, Elbe-Elster, Havelland, Märkisch-Oderland, Oberhavel, Oberspreewald-Lausitz, Oder-Spree, Ostprignitz-Ruppin, Potsdam-Mittelmark, Prignitz, Spree-Neiße, Teltow-Fläming, Uckermark, Rostock, Hansestadt, Schwerin, Landeshauptstadt, Mecklenburgische Seenplatte, Landkreis Rostock, Vorpommern-Rügen, Nordwestmecklenburg, Vorpommern-Greifswald, Ludwigslust-Parchim, Chemnitz, Erzgebirgskreis, Mittelsachsen, Vogtlandkreis, Zwickau, Bautzen, Görlitz, Meißen, Sächsische Schweiz-Osterzgebirge, Leipzig, Kreis, Nordsachsen, Dessau-Roßlau, Altmarkkreis Salzwedel, Anhalt-Bitterfeld, Börde, Burgenlandkreis, Harz, Jerichower Land, Mansfeld-Südharz, Saalekreis, Salzlandkreis, Stendal, Wittenberg, Gera, Jena, Suhl, Weimar, Eisenach, Eichsfeld, Nordhausen, Wartburgkreis, Unstrut-Hainich-Kreis, Kyffhäuserkreis, Schmalkalden-Meiningen, Gotha, Sömmerda, Hildburghausen, Ilm-Kreis, Weimarer Land, Sonneberg, Saalfeld-Rudolstadt, Saale-Holzland-Kreis, Saale-Orla-Kreis, Greiz, Altenburger Land </li>
    <strong>Cluster 2: </strong> Hamburg, Berlin </li>
    <strong>Cluster 3: </strong> Kiel, Landeshauptstadt, Lübeck, Hansestadt, Braunschweig, Hannover, Bremen, Düsseldorf, Duisburg, Essen, Krefeld, Mönchengladbach, Oberhausen, Wuppertal, Mettmann, Rhein-Kreis Neuss, Wesel, Bonn, Köln, Aachen, Rhein-Erft-Kreis, Rhein-Sieg-Kreis, Gelsenkirchen, Münster, Borken, Recklinghausen, Steinfurt, Bielefeld, Gütersloh, Bochum, Dortmund, Herne, Ennepe-Ruhr-Kreis, Märkischer Kreis, Unna, Kreisfreie Stadt Darmstadt, Kreisfreie Stadt Frankfurt am Main, Kreisfreie Stadt Offenbach am Main, Landeshauptstadt Wiesbaden, Groß-Gerau, Main-Kinzig, Offenbach, Kreisfreie Stadt Kassel, Stadt Ludwigshafen a. Rh., Stadt Mainz, Stuttgart, Böblingen, Esslingen, Ludwigsburg, Rems-Murr-Kreis, Karlsruhe, Stadt, Karlsruhe, Kreis, Heidelberg, Mannheim, Rhein-Neckar-Kreis, Freiburg im Breisgau, Ortenaukreis, München, Landeshauptstadt, Rosenheim, Stadt, München, Kreis, Regensburg, Stadt, Nürnberg, Augsburg, Stadt, Regionalverband Saarbrücken, Dresden, Leipzig, Stadt, Halle (Saale), Magdeburg, Erfurt </li>

  </ul>
</details>
