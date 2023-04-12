const CurDrtBid 	=   "jdDartBoard" ;
const jsonSegArr    =   dbjson();	
const defWidth 		= 	500
const minWidth 		= 	250

if( !jsonSegArr || (jsonSegArr.length==0) ){

	// jsonSegArr = dbjson(); // this is the function that creates the segment array in json format
	console.log( "No dartboard jsonSegArr available")

}

// else{          console.log( "dartboard jsonSegArr available)" )
// , createDartBoard() }



if( !scoreArr ){ 
	
	console.log("ndp.js scoreArr doesn't exist (yet)" ); 

}else{

	if( getDN(121)==3 ){

		console.log("dbCreate.js getDN(121)==3" ); 

	}else{

		console.log("dbCreate.js getDN(121) else" ); 		

	}
}




function sendDartToPy(daboNr, segId, ttl ){
	console.log("sendDartToPy daboNr: ", daboNr, "\tsegId:\t" + segId );
	
	let pyXhttp = new XMLHttpRequest() ;
	
	pyXhttp.open("GET", "/input/" + daboNr + "/" + segId, true) ;
	pyXhttp.send() ;

	pyXhttp.onreadystatechange=function(){
		if( (this.readyState == 4) && (this.status == 200) ){
			let pyReply = JSON.parse( this.responseText );
			if( pyReply.status == "success" ){ 
				// d3.select("body").style("backgroundColor: "+pyReply.bgColor+";" )
				console.log("pyXhttp.onreadystatechange pyReply:", pyReply );
				d3.select("#dabo").style("background-color", pyReply.bgColor )
				d3.select("#"+segId).style("fill", "#ff00ff")
				document.title = ttl; 
			}
		}
	}
}


function createDartBoard(dim){
	let wrapperW = defWidth
	if(dim){ wrapperW = parseInt(dim); }
	// dartboard size is set in css according to device and orientation
	const divW      =   d3.min([wrapperW * 0.55, minWidth]);
	const divH      =   d3.min([wrapperW * 0.55, minWidth]);
	const ActDim    =   divW;
	const JDDbCntr  =   (ActDim * 0.5 ) ; /* absolute center for transform-translate purposes */
	const JDDbR     =   (ActDim * 0.4995) ;	
	console.log("divW", divW, "divH", divH    );
	/*  txtArcW:
		The difference from dbData.js segRadPerc[5] - segRadPerc[4] = 0.11. 
		Can be adjusted here for smaller or bigger text in outside ring (JDDbMDOTxtSz).
	*/
	const txtArcW = 0.11;
	const JDDbMDOTxtSz = ( ( (JDDbR * txtArcW ) / 21) * 0.85) ;

	// clean up previous svg dartboard elements when rebuilding/refreshing
	d3.select(".JDDbCanvas").remove();
	d3.select(".dartboardbg").remove();
	d3.select(".JDDbSgmnt").remove();
	d3.select(".JDDbSegment").remove();
	d3.select(".JDDMDOTxt").remove();

	// setting a container for all svg elements
	const mySvg = d3.select( "#mySVGdartBoard")
				.attr("width",  ActDim  )
				.attr("height", ActDim  )
					.append("svg")
						.attr("x", 		"1px"           )
						.attr("y", 		"1px"           )
						.attr("width", 	ActDim          )
						.attr("height", ActDim          )
						.attr("fill", 	"#000000"       )
						.attr("id",     CurDrtBid       )
						.attr("class", 	"JDDbCanvas"    )
	;


	// setting a background for the dartboard
	d3.select( ".JDDbCanvas" )
		.append("rect")
			.attr("x", '0px')
			.attr("y", '0px') 
			.attr("width", (ActDim))
			.attr("height", (ActDim))
			.attr("id", "dartboardbg")
			.attr("fill", "#000000") // #99ff66
	;
	
	// JDDbSgmntGrp will contain the path elements
	const JDDbSgmntGrp  =   d3.select(".JDDbCanvas")
								.append("g")
									.attr("id", "JDDbSgmnts")
									.attr("class", "JDDbSgmnt")
									.attr("stroke-width", 0)
									.attr("stroke", "#C0C0C0")
									.attr("transform", "translate(" + JDDbCntr + "," + JDDbCntr + ")")
							;
	
	// JDDbSgmntGrp will contain the text elements
	const JDDbSgmntTxtGrp   =   d3.select( ".JDDbCanvas" )
									.append("g")
										.attr("id", "JDDbSgmntTxts")
										.attr("class", "JDDMDOTxt")
										.attr("stroke", "#FFFFFF") // #FFFFFF = white 
										.style("font-family", "helvetica")
										.style("font-size", JDDbMDOTxtSz + "em")
										.attr("stroke-width", 2)
										.attr("style", "stroke:#000000;")	// silver #C0C0C0
										.attr("style", "fill:#99CCFF;")		// #00FFFF
										.attr("text-anchor", "middle")
										.attr("transform", "translate(" + JDDbCntr + "," + JDDbCntr + ")")
							;
	
	// Here the magic (creating paths) happens with the data from the jsonSegArr (dbData.js)
	let JDDbSgmntArc    =   d3.arc()
								.innerRadius(   function(data){ return (JDDbR * data.segInRad);})
								.outerRadius(   function(data){ return ((JDDbR * 0.995) * data.segOutRad);})
								.startAngle(    function(data){ return (data.segSA * (Math.PI/180)); }) 
								.endAngle(      function(data){ return (data.segEA * (Math.PI/180)); }) 
							;

	// starting dartboard build paths
	JDDbSgmntGrp.selectAll("path")
		.data(jsonSegArr) // starting the json data loop here jsonSegArr
			.enter()
				.append("path")
					.attr("d", JDDbSgmntArc )
					.attr("id",         (data)=>{ return data.segId; })
					.attr("segId",      (data)=>{ return data.segId; })
					.attr("segVal",     (data)=>{ return data.segVal;  })
					.attr("segGrp",     (data)=>{ return data.segGrp; })
					.attr("segMulti",   (data)=>{ return data.segMulti; })
					.attr("style",      (data)=>{ return "fill:" + data.segColor + ";"; } ) 
					.attr("segColor",   (data)=>{ return data.segColor; } )
					.attr("jdcolored", 'false') 
					.attr("class", 'JDDbSegment' )
					.on('click', FnSegmentClick )
					.on("mouseover", segHover )
					.on("mouseout", segUnHover )	
	;
	
	// adding dartboard text elements (outside-ring)
	JDDbSgmntTxtGrp.selectAll("text")
		.data(jsonSegArr)
			.enter()
				.append("text")
					.filter( (d)=>{ return d.segMulti < 1; })
					.attr("transform", 
							(d)=>{ 
									d.innerRadius = (JDDbR * d.segInRad);
									d.outerRadius = (JDDbR * d.segOutRad);
									return "translate(" + JDDbSgmntArc.centroid(d) +") rotate(" + 1 + ")";
							}
					)
					.text( (d)=>{ return parseInt(d.segGrp,10); })
					.attr("dx",1)	//	JDDbCntr
					.attr("dy",5)	//	JDDbCntr	
					.attr("id", ( (d)=>{ return d.segId; } ) )
					.attr("segVal", '0' )
					.attr("segGrp", '0' )
					.attr("segMulti", '0' ) 
					.attr("class",'JDDbSegment' )
					.on("click", FnSegmentClick )
					/*
					.on("mouseover", segHover )
					.on("mouseout", segUnHover )
					*/
	;
} // End of fn createDartBoard



function whichDart(){
	let serverUrl = location.href.split("/")[ location.href.split("/").indexOf("dabo") + 1 ];
	console.log("whichDart = ", serverUrl )
	return serverUrl;
}


function FnSegmentClick(d,i,e){
	/* 
		d = data of the element from jsonSegArr.
		i = the index of that data in jsonSegArr.
		e = the path/text element with it's attributes and properties.
	*/
	const ClickedSegment = d ;
	let daboNr = whichDart();
	let ttl = "#" + daboNr.toString() + "-" + ClickedSegment.segId
	sendDartToPy(daboNr, ClickedSegment.segId, ttl );

	let msg =  "dabo #" + daboNr + "\t"+ ClickedSegment.segId + " = " + ClickedSegment.segVal ;
	d3.select("#pgTtl").text(msg);
	let curMsgCount =   d3.selectAll(".dbMsgT").size() ;

	if(curMsgCount >= 3){ 
		d3.selectAll(".dbMsgT").remove(); 
		console.log("curMsgCount", curMsgCount, "removed")
	}else{
		console.log("curMsgCount", curMsgCount, "no segclickmsg to remove")
	}

	console.log("curMsgCount", d3.selectAll(".dbMsgT").size() )
	
	d3.select("#msgCenter" )
		.append("div")
			.text( msg )
			.attr("class","dbMsgT")
		;

	console.log( "FnSegmentClick: \nClickedSegment: ", msg );
}


function segHover(d,i,e){
	// shows the value of the segment, the score after, and darts needed after  
	const trgt      = d3.select("#trgtInfo") ;
	const scrsAv    = 121 ; // ( scores.length > 0 ) ;
	const sbInt     = 121 ;
	const sbDN      = getDN(sbInt) || 3 ;
	const saDN      = getDN(sbInt-d.segVal) || 3 ;
	let trgtTxt     = " ";

	if( scrsAv && sbInt ){
		 trgtTxt = d.segId + " (" +  d.segVal + ") leaves " + ( sbInt - d.segVal ) + " = " + saDN + " darter" ;
	}else{
		trgtTxt  = "not available (scores info or Score Before)";
	}
	
	// console.log( "hovering", d.segId, "scrsAv",   scrsAv, "sbDN",     sbDN , "\ntrgtTxt", trgtTxt );
	d3.select("#trgtInfo").text( trgtTxt );

}


function segUnHover(){
	d3.select("#trgtInfo")
			.attr("opacity", "0")
			.text("no segment selected")
		;
}

// createDartBoard(defWidth)