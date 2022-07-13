# -*- coding: utf-8 -*-
#
# Francois M
#
# Lib create an offline html file to
# open these tiles offline
# Also contains tile and image manipulation functions
#

import glob
import os
import shutil


def ge_rearrange(dirlist=[], outputdir="ve_tiles", inputdir="./stiles"):
    """

    Moves tiles acquired from mapTiler into outputdir directory.
    the mapTiler tiles  are stored in directories corresponding to dates.
    All these directories must be put into a single inputdir

    """
    d = os.getcwd()
    print(d)
    p = outputdir
    try:
        os.mkdir(p)
    except:
        pass

    #
    # Goes throuh the inputdir treefile and
    # replicates the directories into the outputdir
    #

    #
    # goes through each mapTiler directory
    #
    directorylist = glob.glob(inputdir + "/*")
    print(directorylist)
    for directory in directorylist:
        #
        # then replicates the zoom levels
        #
        zoom_level = glob.glob(directory + "/*")
        for zoom in zoom_level:

            sd = zoom.split("/")[3]
            print("z:", sd)
            try:
                os.mkdir(p + "/" + sd)
            except:
                pass

            xl = glob.glob(zoom + "/*")
            for x in xl:
                print(x)
                ssd = x.split("/")[4]
                print("x:", ssd)
                try:
                    os.mkdir(p + "/" + sd + "/" + ssd)
                except:
                    pass

                ifiles = glob.glob(x + "/*")

                #
                # copies the Tiles
                #
                for ifile in ifiles:

                    dest_file = p + "/" + sd + "/" + ssd + "/" + ifile.split("/")[5]
                    print(dest_file)
                    shutil.copyfile(ifile, dest_file)


def ge_transform(dirlist=["sat_tiles"]):
    """
    Converts google satellite tiles into osm format tiles.

    """
    d = os.getcwd()
    print(d)
    p = "ve_tiles"
    try:
        os.mkdir("ve_tiles")
    except:
        pass

    directorylist = dirlist
    for directory in directorylist:
        zoom_level = glob.glob(directory + "/*")
        for zoom in zoom_level:
            print(zoom)
            osm_zoom = 17 - int(zoom.split("/")[1])
            p1 = p + "/" + str(osm_zoom)
            print(p1)
            try:
                os.mkdir(p1)
            except:
                pass

            xl = glob.glob(zoom + "/*")
            for x in xl:
                print(x)
                x_ori = (
                    int(x.split("/")[2]) * 1024
                )  # taille de l'image semble moins grande que 1024 pourtant

                xxl = glob.glob(x + "/*")
                for xx in xxl:
                    print(xx)
                    coord_x = x_ori + int(xx.split("/")[2])
                    # ~ print( xx, coord_x )
                    p2 = p1 + "/" + str(coord_x)
                    try:
                        os.mkdir(p2)
                    except:
                        pass

                    yl = glob.glob(xx + "/*")
                    print(yl)
                    for y in yl:
                        y_ori = int(y.split("/")[4]) * 1024
                        print(y, y_ori)

                        yyl = glob.glob(y + "/*")
                        for yy in yyl:
                            yynumber = (yy.split("/")[5])[:-4]
                            coord_y = y_ori + int(yynumber)
                            dest_file = p2 + "/" + str(coord_y) + ".png"
                            print(yy, dest_file)
                            shutil.move(yy, dest_file)


def pic_rename():
    """
    rename_pictures into p_date_time.jpg
    """
    import PIL.Image
    import PIL.ExifTags

    directory = "./images"
    filename = glob.glob(directory + "/*")
    print(filename)
    for f in filename:
        img = PIL.Image.open(f)

        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }

        dt = exif["DateTimeOriginal"]
        dt = dt.replace(" ", "_").replace(":", "")
        print(dt)
        destfile = "./Eric/guilin_" + dt + ".jpg"
        shutil.move(f, destfile)


def create_html(
    offlineName="IPGPOffline",
    sitename="IPGP Offline",
    tiledir="ve_tiles",
    center_lat=48.844740,
    center_lon=2.356265,
    zoom_level=17,
    max_native_zoom=19,
):
    """
    Creates an offlieName directory and an OfflineName.html file
    within that directory
    copies the js libraries into the offlineName directory

    to complete the processs you must then place the tile files tree in the
    offlineName directory

    see example
    """

    try:
        os.mkdir(offlineName)
    except:
        pass

    try:
        shutil.copytree("./lib", "./" + offlineName + "/lib")
    except:
        pass

    f = open(offlineName + "/" + offlineName + ".html", "w")

    site_str = """
    <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="utf-8">
                <meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no' />
    """
    f.write(site_str)

    site_str = "<title>%s</title>\n" % (offlineName)
    f.write(site_str)

    site_str = """
                <!-- Leaflet -->
                <link rel="stylesheet" href="./lib/leaflet/leaflet.css" />
    			<script src="./lib/leaflet/leaflet.js"></script>
    			<script src="./lib/leaflet.ajax.min.js"></script>

                <style>
                    body { margin:0; padding:0; }
                    body, table, tr, td, th, div, h1, h2, input { font-family: "Calibri", "Trebuchet MS", "Ubuntu", Serif; font-size: 11pt; }
                    #map { position:absolute; top:0; bottom:0; width:100%; z-index:1 ;} /* full size */
                    .ctl {
                        padding: 2px 10px 2px 10px;
                        background: white;
                        background: rgba(255,255,255,0.9);
                        box-shadow: 0 0 15px rgba(0,0,0,0.2);
                        border-radius: 5px;
                        text-align: right;
                    }
                    .title {
                        font-size: 18pt;
                        font-weight: bold;
                    }
                    .src {
                        font-size: 10pt;
                    }

    				.command {
    					background:#BDDBBB;
    					padding:5px;
    				}

    				.command:hover{
    					background:#DBBDBB;
    				}

    				.menu {
    					float: right;
    					overflow: hidden;
    				}

    				.menu .menubtn {
    					position: relative; top:0;
    					background:#FFFFFF;
    					width:100px;
    					padding:10%;
    					display: inline-block;
    					z-index:2;
    					text-align:center;
    				}
    				.menu-content {
    					display: none;
    					position: absolute;
    					max-width=150px;
    					background-color: #FFFFFF;
    					box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    					padding: 1%;
    					z-index: 2;
    				}

    				.show {display: block;}

    				li {
    					display: inline;
    				}

                </style>

            </head>
            <body>
    		<div id="map"></div>
    			<div class="menu">
    				<button onclick="dropdown()" class="menubtn">Options</button>
    				<div id="mymenu" class="menu-content">
    					<form class="myform">
    						<input id="clickPosition" type="checkbox"/>Coords<br>
    						<input id="locatePosition" type="checkbox"/>Locate<br>
    						<input id="showPosition" type="checkbox"/>Show Position<br>
    						<input id="trackPosition" type="checkbox"/>Track
    					</form>
    				</div>
    			</div>
    			<div class="menu">
    				<button onclick="Center()" class="menubtn">Center</button>
    			</div>

    			</div>

            <script>

    		/* 3.14

    		compass before heading for azimuth
    		added a red icon on error.

    		*/


    		/* Menu */
    		/* When the user clicks on the button,
    		toggle between hiding and showing the dropdown content */
    		function dropdown() {
    			document.getElementById("mymenu").classList.toggle("show");
    		}

    		function dropdownmap() {
    			document.getElementById("mymaps").classList.toggle("show");
    		}


           /*  Map  */

            var map = L.map('map', {"""
    f.write(site_str)

    site_str = "center: [ %f,%f],\n zoom: %i," % (center_lat, center_lon, zoom_level)
    f.write(site_str)

    site_str = """   minZoom: 1,
                maxZoom: 25,

                //maxNativeZoom:19 ,
                zoomControl: true
            });


    		/* Tiles and layers */
            """
    f.write(site_str)
    site_str = (
        "var ve = L.tileLayer('./%s/{z}/{x}/{y}.png', {opacity: 1, maxNativeZoom:%i,maxZoom:25}).addTo(map);"
        % (tiledir, max_native_zoom)
    )
    f.write(site_str)

    site_str = """
            var ve_layer;


    		/*
    		var geojson_layer = new L.GeoJSON.AJAX("guilin_lib.geojson");
    		geojson_layer.bindPopup(function (layer) {
    			return '<b>'+layer.feature.properties.name + '</b><br><img src=" + layer.feature.properties.link + ' width="150px"/>';
    			});
    		*/



    		/* Icons */

    		function createIcon(locate,heading){

    			var radius=10;
    			var dr=1.5*radius;
    			var x=20;
    			var y=20;
    			var w=40;
    			var h=40;

    			//console.log(heading);

    			if (heading>=0){
    				//console.log('here');
    				var theta=heading*Math.PI/180;
    				var x2=x+dr*Math.sin(theta);
    				var y2=y-dr*Math.cos(theta);
    			}
    			else{
    				//console.log('there');
    				var x2=x;
    				var y2=y;
    			}

    			//console.log(x,y,x2,y2);

    			if (locate===true) {
    				var fillColor='LightSkyBlue';
    			}
    			else {
    				var fillColor='Red';
    			}

    			var svgCircle= "<svg xmlns='http://www.w3.org/2000/svg' version='1.1' width='"+w.toString()+"' height='"+h.toString()+"'>"+
    			"<line x1='"+x.toString()+"' y1='"+y.toString()+"' x2='"+x2.toString()+"' y2='"+y2.toString()+"' stroke='blue'  stroke-width='4' />"+
    			"<circle cx='"+x.toString()+"' cy='"+y.toString()+"' r='10' stroke='black' stroke-width='2' fill='"+fillColor+"'  fill-opacity='0.4'/></svg>";

    			var svgURL = "data:image/svg+xml;base64," + window.btoa(svgCircle);

    			var svgIcon = L.icon({
    				iconUrl: svgURL,

    				iconSize:     [w,h], // size of the icon
    				iconAnchor:   [x, y], // point of the icon which will correspond to marker's location
    				popupAnchor:  [x, y] // point from which the popup should open relative to the iconAnchor
    				});

    			return svgIcon;
    		}




    		//var hotel = L.marker([25.272827, 110.305413]).addTo(map);
    		//hotel.bindPopup("Parkside Hotel");


    		// Popup to display coordinates of points on the map
    		var popup= L.popup();


    		function onMapClick(e){
    			if (document.getElementById ("clickPosition").checked) {
    				//copy clicked position to clipboard
    				var locText=e.latlng.toString();
    				// place in popup
    				popup
    					.setLatLng(e.latlng)
    					.setContent(locText)
    					.openOn(map);
    			}
    		}

    		map.on('click',onMapClick);

    		/* Positioning */

    		// Placeholders for the L.polyline and L.circle representing user's current position and accuracy
    		var current_position;
    		var pos;
    		var compassdir;
    		var azim

    		function onLocationFound(e) {
    		  // if position defined, then remove the existing position marker  from the map
    		  if (current_position) {
    			  map.removeLayer(current_position);
    		  }
    		  // places latlng in pos
    		  pos=e.latlng
    		  if (document.getElementById("showPosition").checked){
    			if (compassdir){
    				azim=compassdir;
    			}
    			else {
    			  if (e.heading) {
    				azim=e.heading;
    			  }}

    			  var blueIcon=createIcon(true,azim);
    			  current_position = L.marker(pos,{icon:blueIcon}).addTo(map);
    			}
    			// test for tracking
    		  if (document.getElementById ("trackPosition").checked) {
    			map.setView(pos);
    			}
    			// end location found
    		}

    		function onLocationError(e) {
    		  if (current_position) {
    			  map.removeLayer(current_position);
    		  }
    		  if (document.getElementById("showPosition").checked && pos){
    			  var redIcon=createIcon(true,azim);
    			  current_position = L.marker(pos,{icon:redIcon}).addTo(map);
    		  }

    		}


    		map.on('locationfound', onLocationFound);
    		map.on('locationerror', onLocationError);

    		/* Event handling */


    		/* Launch tracking */
    		function handleTrackingCommand() {
    				if  (document.getElementById ("trackPosition").checked){
    						map.setView(pos);
    				}
    			}
    		/* Show position marker */
    		function handleShowCommand() {
    			if  (document.getElementById ("showPosition").checked && current_position){
    			  map.removeLayer(current_position);
    			  if (document.getElementById("locatePosition").checked){
    				  var blueIcon = createIcon(true,azim);
    				  current_position = L.marker(pos,{icon:blueIcon}).addTo(map);
    				  }
    			  else {
    				  var redIcon = createIcon(false,azim);
    				  current_position = L.marker(pos,{icon:redIcon}).addTo(map);
    				  }
    			  }
    			 else {
    				 map.removeLayer(current_position);
    			 }
    		}

    		/* Launch positioning */
    		function handleLocateCommand(){
    			if (document.getElementById("locatePosition").checked){
    				map.locate({setView: false, maxZoom: map.getZoom(), watch:true, enableHighAccuracy:true});
    			}
    			else {
    				map.stopLocate();
    				if  (document.getElementById ("showPosition").checked){
    					map.removeLayer(current_position);
    					var redIcon=createIcon(false,azim);
    					current_position = L.marker(pos,{icon:redIcon}).addTo(map);
    				}
    			}
    		}

    		function Center() {
    				map.setView(pos);
    		}



    		function handleLandsatCommand(){
    			//landsat image
    			if (document.getElementById ("landsat").checked){
    				landsat_layer = landsat.addTo(map);
    			}
    			else {
    				map.removeLayer(landsat_layer);
    			}
    		}

    		function handleOSMCommand(){
    			// osm layer
    			if (document.getElementById ("osm").checked){
    				osm_layer=osm.addTo(map);
    			}
    			else {
    				map.removeLayer(osm_layer);
    			}

    		}


    		function handleVECommand(){
    			// ve layer
    			if (document.getElementById ("ve").checked){
    				ve_layer=ve.addTo(map);
    			}
    			else {
    				map.removeLayer(ve_layer);
    			}

    		}

    		if (window.DeviceOrientationEvent) {
    			console.log('ici');
    		// Listen for the deviceorientation event and handle the raw data
    			window.addEventListener('deviceorientation', function(eventData) {
    				if(event.webkitCompassHeading) {
    				// Apple works only with this, alpha doesn't work
    					compassdir = event.webkitCompassHeading;
    					consol.log(compassdir);
    				}
    				//else compassdir = event.alpha;
    			});
    		}


    		/*
    		function handlePicturesCommand(){
    			// Field pictures
    			if (document.getElementById ("pictures").checked){
    				console.log('ici');
    				geojson_layer.addTo(map);
    			}
    			else {
    				map.removeLayer(geojson_layer);
    			}

    		}
    		*/

    		document.getElementById ("trackPosition").addEventListener ("click", handleTrackingCommand, false);
    		document.getElementById ("showPosition").addEventListener ("click", handleShowCommand, false);
    		document.getElementById ("locatePosition").addEventListener ("click", handleLocateCommand, false);
    		document.getElementById ("ve").addEventListener ("click", handleVECommand, false);
    		//document.getElementById ("pictures").addEventListener ("click", handlePicturesCommand, false);


    	</script>

      </body>
    </html>



    """
    f.write(site_str)
    f.close()


if __name__ == "__main__":
    ge_rearrange()
