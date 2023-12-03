import gpxpy
import geojson
import os
import re

def extract_elevation_up(desc):
    # Use regular expression to extract elevation up from the desc string
    match = re.search(r'Elevation up: (\d+(\.\d+)?)m', desc)
    if match:
        return float(match.group(1))
    else:
        return None

def search_passi_file(idd, passi_file_path):
    # Search for idd in the "passi" file
    with open(passi_file_path, 'r') as passi_file:
        for line in passi_file:
            if f'"idd":"{idd}"' in line:
                return True
    return False

def add_new_element_to_file(idd, height, passName, category, country, passLink, long, lat, output_file_path):
    # Write the new element to the "NewElements.txt" file
    new_element = f'{{"type":"Feature","properties":{{"idd":"{idd}","height":"{height}","name":"{passName}","category":"{category}","country":"{country}","link":"{passLink}"}}, "geometry":{{"type":"Point","coordinates":[{long}, {lat}]}}}},'
    with open(output_file_path, 'a') as new_elements_file:
        #new_elements_file.write(new_element)
        new_elements_file.seek(0, os.SEEK_END)
        new_elements_file.write(new_element)

def gpx_to_geojson(gpx_file_paths, output_directory, passi_file_path):
    features = []
    passi_check_counter = 0
    gpx_file_name = os.path.splitext(os.path.basename(gpx_file_paths[0]))[0]
    
    idd = input("Enter idd for {}: ".format(gpx_file_name))
    category = input("Enter category for {}: ".format(gpx_file_name))
    country = input("Enter country for {}: ".format(gpx_file_name))

    for gpx_file_path in gpx_file_paths:
        # Check if idd exists in "passi" file
        if passi_check_counter == 0 and not search_passi_file(idd, passi_file_path):
            passi_check_counter += 1
            passName = input("Enter passName for {}: ".format(gpx_file_path))
            passHeight = input("Enter height for {}: ".format(gpx_file_path))
            passLink = input("Enter passLink for {}: ".format(gpx_file_path))
            
            with open(gpx_file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                last_trackpoint = gpx.tracks[0].segments[0].points[-1]
                long = last_trackpoint.longitude
                lat = last_trackpoint.latitude

            # Add new element to "NewElements.txt" file
            add_new_element_to_file(idd, passHeight, passName, category, country, passLink, long, lat, "NewElements.txt")
        
        name = input("Enter name for {}: ".format(gpx_file_path))
        link = input("Enter link for {}: ".format(gpx_file_path))

        

        with open(gpx_file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                coordinates = [(point.longitude, point.latitude, point.elevation) for point in segment.points]
                line_string = geojson.LineString(coordinates)
                
                distance = round(track.length_3d()/1000, 1)

                # Extract elevation-up from desc
                elevation_up = round(extract_elevation_up(track.description),0)

                # Add properties to the GeoJSON feature
                properties = {
                    "idd": idd,
                    "name": name,
                    "length": distance,
                    "elevation": elevation_up,
                    "category": category,
                    "country": country,
                    "link": link
                }

                feature = geojson.Feature(geometry=line_string, properties=properties)
                features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    write_leaflet_code_to_file(feature_collection, output_directory)
    
    return feature_collection

def write_leaflet_code_to_file(geojson_data, output_directory):
    # Get input from the user for XX
    XX = input("Enter variable name: ")
    geojson_str = geojson.dumps(geojson_data, indent=2)
    modified_geojson_str = f"var {XX} = {geojson_str}"
    geojson_data = modified_geojson_str
    # Create the Leaflet JavaScript code string
    leaflet_code = f"""
var g{XX} = L.geoJSON({XX}, {{
    style: TrackStyle,
    onEachFeature: onEachFeature
}});
var id{XX} = {XX}.features[0].properties.idd;
geoJSONArray[id{XX}] = g{XX};
geoJSONs.push(g{XX});
"""
    # Write the code to a text file
    output_file_path = os.path.join(output_directory, f"{XX}.js")
    with open(output_file_path, 'w') as output_file:
        #geojson.dump(geojson_data, output_file)
        output_file.write(modified_geojson_str)
    
    output_text_file_path = "variableTags.txt"
    with open(output_text_file_path, 'a') as output_file:
        output_file.write(leaflet_code)
        
    script_tag = f'<script src="Tracks/{XX}.js"></script>\n'
    script_file_path = "scriptTags.txt"
    with open(script_file_path, 'a') as script_file:
        script_file.write(script_tag)
#################################################################################################################
output_directory = "GeoTracks/"
gpx_files = [
#"Komoot/FinstertalerStausee 3.56 380-1383324335.gpx",
#"Komoot/Tougnete 6.69 590-1383323414.gpx",
#"Komoot/LagoNaret 32.0 1930-1383327525.gpx",
#"Komoot/LacDuSaut 5.68 460-1383328828.gpx",
#"Komoot/AlpeGalm 15.0 1330-1383332374.gpx",
#"Komoot/MännlichenVonGrindelwald 12.9 1270-1383332958.gpx",
#"Komoot/Täschalp 7.16 760-1383334126.gpx",
#"Komoot/ObereFeselalp 18.3 1570-1383334598.gpx",
#"Komoot/RifugioForni 5.56 400-1383335294.gpx",
#"Komoot/StauseeMattmark 11.0 630-1383334756.gpx",
#"Komoot/BarrageDeLaGrandeDixence 18.8 1220-1383336104.gpx",
#"Komoot/RifugioCinqueTorri 4.2 380-1383336702.gpx",
#"Komoot/Tignes 7.41 350-1383337017.gpx",
#"Komoot/BerghausNagens 8.95 1060-1383337373.gpx",
#"Komoot/Juf 24.2 1100-1383337588.gpx",
#"Komoot/TignesAlt 11.9 600-1383337157.gpx",
#"Komoot/Arc2000 24.1 1390-1383338397.gpx",
#"Komoot/Belpiano 9.74 630-1383339537.gpx",
#"Komoot/SpeikkogelViaKoralpe15.6 1650-1383337986.gpx",
#"Komoot/ArollaValHerens 37.1 1630-1383340113.gpx",
#"Komoot/ColDuSabot 14.7 1330-1383339708.gpx",
#"Komoot/Hochsölden 3.61 370-1383340292.gpx",
#"Komoot/Martelltal 22.8 1440-1383340511.gpx",
#"Komoot/TauernmoosStauseeViaEnzingerBoden 22.6 1340-1383340933.gpx",
#"Komoot/ColleDelPreit 10.1 850-1383341165.gpx",
#"Komoot/LaPlagne 17.9 1310-1383342940.gpx",
#"Komoot/Thyon2000Sion 18.0 1380-1383341581.gpx",
#"Komoot/Thyon2000Vex 14.5 1160-1383341439.gpx",
#"Komoot/ColleSanCarloMorgex 10.3 1010-1383343595.gpx",
#"Komoot/ColleSanCarloThuile 7.34 480-1383343531.gpx",
#"Komoot/Mangart 10.9 1010-1383344060.gpx",
#"Komoot/Bettmeralp 15.0 1160-1383345146.gpx",
#"Komoot/LesFonts 11.9 440-1383344958.gpx",
#"Komoot/PartnunViaSt.Antönien 16.4 980-1383344347.gpx",
#"Komoot/LagoDiAlpeGera 17.2 1110-1383345893.gpx",
#"Komoot/SaintVeran 4.85 230-1383345368.gpx",
#"Komoot/SaintVeranAlt 3.89 110-1383345426.gpx",
#"Komoot/Cheneil-1383345961.gpx",
#"Komoot/PianDelRe 19.0 1380-1383349119.gpx",
#"Komoot/Vallée de la Clarée 26.2 680-1383349339.gpx",
#"Komoot/Dischmatal 12.3 460-1383350389.gpx",
#"Komoot/Schnalstal 23.3 1460-1383349991.gpx",
#"Komoot/VenterTal 15.2 580-1383349848.gpx",
#"Komoot/Cervinia 27.8 1550-1383350781.gpx",
#"Komoot/RiedbergZillertalVonKaltenbach 11.2 1230-1383475813.gpx",
#"Komoot/RiedbergZillertalVonRied 12.4 1240-1383475140.gpx",
#"Komoot/MelchbodenZillertalVonAschau 16.6 1530-1383477436.gpx",
#"Komoot/RiedbergZillertalAschau 10.5 1220-1383476604.gpx",
#"Komoot/RiedbergZillteralKalterbachII 12.1 1230-1383476319.gpx",
#"Komoot/MelchbodenZillertalerHöhenstraße 8.33 640-1383481329.gpx",
#"Komoot/MelchbodenZillertalVonAschau 16.1 1510-1383477879.gpx",
#"Komoot/MelchbodenZillertalVonHippach 14.3 1400-1383480751.gpx",
#"Komoot/Hintertux 18.1 870-1383484978.gpx",
#"Komoot/RiedbergZillertalerHöhenstraße 4.34 340-1383481695.gpx",
#"Komoot/DuroneSudOst 7.49 400-1383594701.gpx",
#"Komoot/Hochfügen 13.9 950-1383486179.gpx",
#"Komoot/Zillergrund 22.1 1220-1383485533.gpx",
#"Komoot/BallinoRivaMain 14.4 700-1383597682.gpx",
#"Komoot/DuroneOst 9.33 580-1383595406.gpx",
#"Komoot/DuroneWest 6.81 490-1383595817.gpx",
#"Komoot/BallinoPonteArche 10.0 400-1383599997.gpx",
#"Komoot/BallinoRivaAlt 13.7 700-1383598711.gpx",
#"Komoot/ReiterjochSudVonLavaze 7.48 720-1383606811.gpx",
#"Komoot/LagoMoulinAostaVarI 31.4 1470-1383612111.gpx",
#"Komoot/Plätzwiese 11.5 730-1383609058.gpx",
#"Komoot/ReiterjochNordVonObereggen 4.63 430-1383607350.gpx",
#"Komoot/HochsteinDirettissima 11.0 1150-1383619244.gpx",
#"Komoot/HochsteinLeisach 12.0 1260-1383619868.gpx",
#"Komoot/LagoMoulinAostaVarII 31.1 1440-1383612730.gpx",
#"Komoot/ColDuJoly 21.8 1270-1383623455.gpx",
#"Komoot/HochsteinThal 12.9 1150-1383620488.gpx",
#"Komoot/Jochgrimm 3.54 200-1383621306.gpx",
#"Komoot/ColDuJolyHauteluce 15.7 910-1383627598.gpx",
#"Komoot/PlanD'Aval 5.84 490-1383734442.gpx",
#"Komoot/ValserTalZevrailsee 29.0 1460-1383735549.gpx",
#"Komoot/BarrageDeMauvoisin 19.7 1200-1383740162.gpx",
#"Komoot/MalgaMare 11.4 820-1383738598.gpx",
#"Komoot/Zermatt 36.8 1220-1383744465.gpx",
#"Komoot/ColDeLaForclazSudwest 8.18 450-1383750937.gpx",
#"Komoot/ColDeLaGueulaz 11.5 900-1383748788.gpx",
#"Komoot/SkistationGiw 15.9 1320-1383747135.gpx",
#"Komoot/ColDeLaForclazNordost 13.1 1030-1383751476.gpx",
#"Komoot/LaiDaNalps 9.38 630-1383839491.gpx",
#"Komoot/Valsavarenche 25.8 1340-1383752598.gpx",
#"Komoot/Bormio2000 9.45 720-1383840240.gpx",
#"Komoot/SafientalChur 34.2 1370-1383840977.gpx",
#"Komoot/SafientalIlanz 38.4 1340-1383840807.gpx",
#"Komoot/MontBisanne 14.4 1240-1383845678.gpx",
#"Komoot/RifugioGardeccia 6.2 590-1383841255.gpx",
#"Komoot/MontBisanneSaisies 4.35 370-1383845759.gpx",
#"Komoot/Lü 3.82 330-1383846851.gpx",
#"Komoot/SilzerBerg 12.1 1260-1383847809.gpx",
#"Komoot/Sertigtal 7.25 360-1383848596.gpx",
#"Komoot/SertigtalDavos 8.27 370-1383848651.gpx",
#"Komoot/Stallwieshof 8.92 640-1383848392.gpx",
#"Komoot/GlocknerLucknerHaus 20.8 1160-1383849213.gpx",
#"Komoot/LagoDiTeleccio 12.0 1190-1383849415.gpx",
#"Komoot/Lüsens 8.31 450-1383848855.gpx",
#"Komoot/Praxmar 6.67 490-1383848805.gpx",
#"Komoot/Kölnbreinsperre 29.5 1220-1383849595.gpx",
#"Komoot/LangtaufenerTal 10.1 410-1383850515.gpx",
#"Komoot/Vallée de l'Ubaye 12.8 470-1383850739.gpx",
#"Komoot/MadoneDeFenestre 12.6 960-1383851122.gpx",
#"Komoot/Melchtal 25.3 1480-1383851257.gpx",
#"Komoot/Sulden 11.1 660-1383850903.gpx",
#"Komoot/CraistasMünstertal 3.03 260-1384076831.gpx",
#"Komoot/CraistasStaMaria 5.86 510-1384076582.gpx",
#"Komoot/Fouillouse 3.55 310-1383851413.gpx",
#"Komoot/SeiserAlmGrödnerTal 8.26 730-1384088222.gpx",
#"Komoot/SeiserAlmPaniderSattel 8.03 510-1384087131.gpx",
#"Komoot/SeiserAlmSeis 9.15 740-1384086645.gpx",
#"Komoot/CiampigottoWestI 16.5 1060-1384094695.gpx",
#"Komoot/CiampigottoWestII 16.1 1050-1384095140.gpx",
#"Komoot/SeiserAlmKastelruth 11.7 790-1384089503.gpx",
#"Komoot/CiampigottoOst 29.6 1320-1384098295.gpx",
#"Komoot/CiampigottoViaSellaDiRioda 29.3 1520-1384096938.gpx",
#"Komoot/MonteLussari 7.73 900-1384100302.gpx",
#"Komoot/SchönfeldsattelMignitz 24.6 860-1384106535.gpx",
#"Komoot/SchönfeldsattelSt.Margareten 20.6 830-1384105974.gpx",
#"Komoot/SchönfeldsattelWest 13.1 750-1384104582.gpx",
#"Komoot/PassoPura 8.07 710-1384114953.gpx",
#"Komoot/TurracherHöheNord 20.8 920-1384109476.gpx",
#"Komoot/TurracherHöheSud 8.47 740-1384109209.gpx",
#"Komoot/PassoCompetLevio 12.1 900-1384251460.gpx",
#"Komoot/PassoPuraLagoSauris 7.02 510-1384115267.gpx",
#"Komoot/ValFerret 12.0 560-1384248946.gpx",
#"Komoot/PassoCompetLevicoBaite 11.2 780-1384252096.gpx",
#"Komoot/PassoCompetOst 10.3 840-1384252645.gpx",
#"Komoot/PassoCompetPergine 13.4 930-1384253678.gpx",
#"Komoot/KientnerAlmWeitental 9.72 880-1384256188.gpx",
#"Komoot/RifugioPanarottaNord-1384254687.gpx",
#"Komoot/RifugioPanarottaViaPassoCompet 4.73 400-1384254008.gpx",
#"Komoot/KientnerAlmMühlbach 13.4 1040-1384258160.gpx",
#"Komoot/KientnerAlmVintl 11.5 970-1384256651.gpx",
#"Komoot/SignalDeLureSud 18.0 1070-1384258857.gpx",
#"Komoot/ObertauernNord 21.3 930-1384262447.gpx",
#"Komoot/ObertauernSud 16.3 600-1384261656.gpx",
#"Komoot/SignalDeLureNord 26.2 1290-1384259206.gpx",
#"Komoot/VillacherAlpenstraße 16.5 1190-1384263739.gpx",
#"Komoot/ZumisLüsen 10.5 840-1384266089.gpx",
#"Komoot/ZumisSüd 10.9 940-1384265717.gpx",
#"Komoot/HofmahdjochNord 9.13 790-1384343005.gpx",
#"Komoot/HofmahdochSud 7.81 720-1384342811.gpx",
#"Komoot/ZumisNord 7.63 720-1384266996.gpx",
#"Komoot/ChamrousseNordWest 17.6 1190-1384344015.gpx",
#"Komoot/ChamrousseSudwest 17.8 1330-1384343457.gpx",
#"Komoot/ChamrousseViaColLuitel 17.2 1370-1384343659.gpx",
#"Komoot/CrêtdeChâtillonSud 13.5 780-1384345259.gpx",
#"Komoot/JouxPlaneNord 10.5 780-1384344724.gpx",
#"Komoot/JouxPlaneSud 11.8 1020-1384344422.gpx",
#"Komoot/JouxPlaneSudAlt 11.4 1000-1384344555.gpx",
#"Komoot/CretDeChatillonNord 16.9 1180-1384345754.gpx",
#"Komoot/CretDeChatillonVieugy 14.1 1060-1384349466.gpx",
#"Komoot/AlpeTeglio 9.16 810-1384351686.gpx",
#"Komoot/Tremalzo 12.9 970-1384349725.gpx",
#"Komoot/ValD'Ayas 31.3 1380-1384350226.gpx",
#"Komoot/ColdelaCouillole 7.21 280-1384353682.gpx",
#"Komoot/ColdelaCouilloleOst 16.2 1200-1384353860.gpx",
#"Komoot/ValbergSudWest 13.4 910-1384354166.gpx",
#"Komoot/GuardaMain 2.87 260-1384355471.gpx",
#"Komoot/GuardaPanoramastraße 4.11 250-1384355606.gpx",
#"Komoot/ValbergNordwest 14.4 890-1384354296.gpx",
#"Komoot/ValbergViaGorgesDuCians 27.9 1410-1384354537.gpx",
#"Komoot/WeinebeneBadSchwanberg 23.7 1290-1384356076.gpx",
#"Komoot/WeinebeneOst 21.6 1320-1384356301.gpx",
#"Komoot/WeinebeneWest 17.9 1200-1384356375.gpx",
#"Komoot/ColDuLoyerOst 6.14 520-1384357358.gpx",
#"Komoot/ColDuLoyerWest 7.5 390-1384356991.gpx",
#"Komoot/ColDuLoyerWestAlt 5.3 380-1384357053.gpx",
#"Komoot/PanthaleonChambave 17.4 1190-1384358368.gpx",
#"Komoot/PanthaleonChambaveAlt 18.0 1190-1384358639.gpx",
#"Komoot/PanthaleonChampagne 20.3 1230-1384358866.gpx",
#"Komoot/ColdeLaPierreduMoëlléSudost 4.22 360-1384361458.gpx",
#"Komoot/ColdeLaPierreduMoëlléSudwest 5.9 540-1384361029.gpx",
#"Komoot/PanthaleonNord 8.24 560-1384359131.gpx",
#"Komoot/BondoneTrento 17.6 1380-1384367074.gpx",
#"Komoot/ColPierreduMoëlléAigle 26.3 1480-1384361894.gpx",
#"Komoot/ColPierreduMoëlléOst 10.9 400-1384361616.gpx",
#"Komoot/Les Deux Alpes 10.3 650-1384362795.gpx",
#"Komoot/BondoneBalsegaBondone 17.4 1160-1384367204.gpx",
#"Komoot/BondoneCadine 16.3 1200-1384367154.gpx",
#"Komoot/BondoneAldeno 23.5 1700-1384368799.gpx",
#"Komoot/BondoneLesino 22.1 1250-1384368588.gpx",
#"Komoot/FtanScuol 4.93 360-1384509013.gpx",
#"Komoot/FtanArdez 6.86 220-1384509294.gpx",
#"Komoot/KlippitztörlOst 14.7 980-1384509771.gpx",
#"Komoot/KlippitztörlSud 23.4 1220-1384510248.gpx",
#"Komoot/KlippitztötlWest 14.1 920-1384511257.gpx",
#"Komoot/ColDeJouxSaintVincent 15.7 1050-1384513860.gpx",
#"Komoot/KatschbergNord 5.41 600-1384513269.gpx",
#"Komoot/KatschbergSud 4.66 460-1384513021.gpx",
#"Komoot/ColDeJouxBrusson 6.0 360-1384514086.gpx",
#"Komoot/MollardNord 16.8 1100-1384514991.gpx",
#"Komoot/MollardSudWest 5.97 390-1384514553.gpx",
#"Komoot/KreuzbergpassNord 14.8 470-1384517713.gpx",
#"Komoot/KreuzbergpassSud 21.2 750-1384516749.gpx",
#"Komoot/MollardNordOst 18.7 1080-1384515415.gpx",
#"Komoot/AbländschenJaun 10.7 610-1384519192.gpx",
#"Komoot/AbländschenSaanen 9.12 590-1384519445.gpx",
#"Komoot/PlateauMoliere 16.3 660-1384520871.gpx",
#"Komoot/ColTzecoreOst 6.31 570-1384521517.gpx",
#"Komoot/ColTzecoreViaColDeJoux 6.02 440-1384521834.gpx",
#"Komoot/PlateauMoliereVonColCroixPerrin 11.8 510-1384521062.gpx",
#"Komoot/AlpeSanBernardo 18.0 1340-1384525038.gpx",
#"Komoot/ColTzecoreSaintVincent 14.1 1020-1384522471.gpx",
#"Komoot/ColTzecoreWest 15.2 1100-1384522988.gpx",
#"Komoot/BaldoMori 22.6 1540-1384530752.gpx",
#"Komoot/ColombiereNordost 17.3 1130-1384526735.gpx",
#"Komoot/ColombiereSudwest 14.2 770-1384527652.gpx",
#"Komoot/BaldoChizolla 22.4 1580-1384532284.gpx",
#"Komoot/BaldoChizollaAlt 25.8 1680-1384532892.gpx",
#"Komoot/BaldoMoriAlt 22.9 1540-1384531285.gpx",
#"Komoot/BaldoAvio 21.1 1520-1384533588.gpx",
#"Komoot/BaldoAvioReverse 23.8 1610-1384533928.gpx",
#"Komoot/BaldoSud 36.9 1760-1384536892.gpx",
#"Komoot/BaldoSudAltII 31.3 1680-1384538362.gpx",
#"Komoot/BalduSudAltI 35.2 1760-1384537667.gpx",
#"Komoot/PuyRichardSudschleife 6.42 400-1384539816.gpx",
#"Komoot/VrsicNord 12.4 870-1384539173.gpx",
#"Komoot/VrsicSud 30.9 1330-1384538952.gpx",
#"Komoot/GurnigelpassNordwest 13.5 610-1384541422.gpx",
#"Komoot/GurnigelpassSudwest 15.6 730-1384540835.gpx",
#"Komoot/PuyRichardNordschleife 5.42 390-1384540044.gpx",
#"Komoot/GurnigelNord 14.7 920-1384542356.gpx",
#"Komoot/GurnigelNordAlt 13.7 850-1384542833.gpx",
#"Komoot/GurnigelPanorama 23.2 710-1384541749.gpx",
#"Komoot/PaniderSattelSt.Ulrich 4.24 270-1384549571.gpx",
#"Komoot/SalseNordost 21.0 1030-1384543445.gpx",
#"Komoot/SalseViaColleSanBernardo 14.3 710-1384543859.gpx",
#"Komoot/PaniderSattelKastelruth 7.38 380-1384550502.gpx",
#"Komoot/ColDeLaMoutiere 14.2 1100-1383303988.gpx",
#"Komoot/Großsee 14.1 1270-1383304641.gpx",
#"Komoot/Hochwurtenspeicher 22.7 1810-1383310756.gpx",
#"Komoot/Granon 11.1 1040-1383311027.gpx",
]

passi_file = "passi.js"

geojson_data = gpx_to_geojson(gpx_files, output_directory, passi_file)
