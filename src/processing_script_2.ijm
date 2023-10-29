
function closeChan(cls_chan){
	print("closing: "+cls_chan);
	selectWindow(getChan(cls_chan));
	close();
}

function getChan(chan_filter){
	list = getList("image.titles");
	for(i = 0;i<list.length;i++){
		if (startsWith(list[i],chan_filter)){
			return list[i];
		}
	}	
}

function process(chan, set_min, set_max, top_out_dir, name){
	selectWindow(chan);
	run("Z Project...", "projection=[Max Intensity]");
	run("Duplicate...", " ");
	saveAs("Tiff", top_out_dir+"/"+name+"_raw.tif");
	close();
	setMinAndMax(set_min, set_max);
	run("Scale Bar...", "width=50 height=4 font=14 color=White background=None location=[Lower Right] bold");
	saveAs("Tiff", top_out_dir+"/"+name+".tif");
	saveAs("Png", top_out_dir+"/"+name+".png");
	return "MAX_"+chan;
}

function get_out_dir_name(image_name){
	out_list = split(image_name," - ");
	/* print(out_list.length); */
	if (out_list.length==1){
		out_list = split(image_name,"...");
	}
	return out_list[1];
}

top_top_out_dir = "/media/scott/Seagate Backup Plus Drive/jordi/processed_images/"
do_trans = 0;

all_images = getList("image.titles");
for (i=0;i<all_images.length;i++) { 
	
	temp_img=all_images[i];
	print("trying to open"+temp_img);
	selectWindow(temp_img);
	print("success");
	out_img_name = get_out_dir_name(temp_img);
	print(out_img_name);
	
	top_out_dir = top_top_out_dir+"/"+out_img_name+"/";
	File.makeDirectory(top_out_dir); 
	
	run("Split Channels");
	wait(200);
	print("closing");
	closeChan("C1-");
	closeChan("C4-");
	print("finding");
	Cxcl10 = getChan("C3-");
	Saa3 = getChan("C5-");
	print("processing");
	/* newly added
	selectWindow(Saa3);
	saveAs("Tiff", top_out_dir+"/"+"Saa3_raw.tif");
	selectWindow(Cxcl10);
	saveAs("Tiff", top_out_dir+"/"+"Cxcl10_raw.tif");
	end newly added */
	processed_cxcl10 = process(Cxcl10, 4000, 65535, top_out_dir, "Cxcl10");
	processed_saa3 = process(Saa3, 4000, 14000, top_out_dir, "Saa3");
	print("merging");
	run("Merge Channels...", "c1=["+"Saa3.png"+"] c2=["+"Cxcl10.png"+"] create");
	selectWindow("Composite");
	saveAs("Tiff", top_out_dir+"/"+"merge.tif");
	saveAs("Png", top_out_dir+"/"+"merge.png");
	if (do_trans==1){
		print("transmitted");
		trans = getChan("C2-");
		selectWindow(trans);
		done_edf = 0;
		do {
			wait (1000);
		} while (isOpen("Output")==0)
		/* Save output */
		closeChan("Height-Map");
		closeChan(trans);
		selectWindow("Output");
		setMinAndMax(5000, 30000);
		run("Set Scale...", "distance=.8809 known=1 unit=microns");
		saveAs("Tiff", top_out_dir+"/"+"EDF_transmitted_light_noSB.tif");
		saveAs("Png", top_out_dir+"/"+"EDF_transmitted_light_noSB.png");
		run("Scale Bar...", "width=50 height=4 font=14 color=White background=None location=[Lower Right] bold");
		saveAs("Tiff", top_out_dir+"/"+"EDF_transmitted_light.tif");
		saveAs("Png", top_out_dir+"/"+"EDF_transmitted_light.png");
		closeChan("EDF");
    } else {
    	closeChan("C2-");
    }
	print("final closing");
	closeChan("merge");
	closeChan("C3-");
	closeChan("C5-");
}



/*
tranmitted = "C2-"+all_images[0];
selectWindow(tranmitted);
run("EDF Easy mode");
run("Wait For User", "Select Rectangle to Invert"); 
selectWindow("Output");
*/


