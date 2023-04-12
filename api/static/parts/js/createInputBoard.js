const CurDrtBid 	=   "inputBoard" ;
const jsonSegArr    =   dbjson();	
const defWidth 		= 	500
const minWidth 		= 	300
let dimUsed 		= 	500

if( !jsonSegArr || (jsonSegArr.length==0) ){ console.log( "createInputDaBo.js No dartboard jsonSegArr available")}

createInputDaBo = (dim)=>{
	let wrapperW = defWidth ;
	if(dim){ wrapperW = parseInt(dim); dimUsed = dim; }
	const divW      =   d3.max([wrapperW*0.925, minWidth]) ;
	const divH      =   d3.max([wrapperW*0.925, minWidth]) ;
	const ActDim    =   divW ;
	const JDDbCntr  =   (ActDim * 0.5 ) ;
	const JDDbR     =   (ActDim * 0.4995) ;	
	console.log("divW", divW, "divH", divH ) ;
	const txtArcW = 0.11 ;
	const JDDbMDOTxtSz = ( ( (JDDbR * txtArcW ) / 21) * 0.85) ;

	d3.select(".JDDbCanvas").remove();
	d3.select(".dartboardbg").remove();
	d3.select(".JDDbSgmnt").remove();
	d3.select(".JDDbSegment").remove();
	d3.select(".JDDMDOTxt").remove();

	// setting a container for all svg elements
	const mySvg = d3.select( "#inputBoard")
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
					.on('click', inputSegClick )	
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
					.on("click", inputSegClick )
	;
} 

inputSegClick = (d,i,e)=>{
	const clickedSegment = d ;
	let daboNr = whichInputDart() ;
	let ttl = "#" + daboNr.toString() + "-" + clickedSegment.segId
	sendDartToPy(daboNr, clickedSegment.segId, ttl ) ;
	console.log( 
		"inputSegClick -> dabo #" , daboNr , 
		"seg: ", clickedSegment.segId , " = ", clickedSegment.segVal 
	) ;
}

sendDartToPy = (daboNr, segId )=>{
	console.log("sendDartToPy daboNr: ", daboNr, "\tsegId:\t" + segId );

	let pyXhttp = new XMLHttpRequest() ;

	pyXhttp.open("GET", "/output/" + daboNr + "/" + segId, true) ;
	pyXhttp.send() ;

	pyXhttp.onreadystatechange = ()=>{

		if( (this.readyState == 4) && (this.status == 200) ){

			let pyReply = JSON.parse( this.responseText );

			if( pyReply.status == "success" ){ 
				console.log("pyXhttp.onreadystatechange pyReply:", pyReply ) ;
				d3.select("#inputBody").style("background-color", pyReply.bgColor ) ;
				createInputDaBo(dimUsed)
			}

		}

	}

}
