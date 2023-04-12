
const colorPairs =  [ 
	{   c1:"#FF00FF",c2: "#FF00FF" },
	{   c1:"#FF6633",c2: "#FF6633" },
	{   c1:"#FF9966",c2: "#FF9966" },
	{   c1:"#0066FF",c2: "#0066FF" },
	{   c1:"#00CCFF",c2: "#00CCFF" }
];

const ndpSeg    =   {
	segId: "",
	NextDartsNeeded: 9,
	ScoreAfterDart: 501,
	NewColor: "#000000"
}

const favDbls = [
	{ seg:"D20", val: 40 }, 
	{ seg:"D16", val: 32 }, 
	{ seg:"DBL", val: 50 }
];

const favTrpls = [
	{ seg:"T20", val: 60 }, 
	{ seg:"T19", val: 57 }, 
	{ seg:"T18", val: 54 }
];

let clrArr = [
	"#006400",  // 0: DarkGreen  same darts needed
	"#00ff00",  // lime          -1 darts needed
	"#ffab00",  // orange        +1 darts needed
	"#ff0000"   // red           bust !
];

let ndpSegArray     =   [];
let jsonSegs 		= 	[];
let scores          =   [];
let numpadDiv       =   document.getElementById('numpad') ;


if( !scoreArr ){ 
	console.log("ndp.js scoreArr doesn't exist" ); 
}else{
	scores = scoreArr;
}


if( !jsonSegArr ){
	console.log("ndp.js jsonSegArr doesn't exist" ); 
}else{
	jsonSegs = jsonSegArr 
}

console.log("ndp.js->scores", scores.length ,"\nndp.js->jsonSegs", jsonSegs.length );

function getDN(score){
	let retvalDN;
	if( score && (score > 0) ){
		if( scores.length>1 ){
			// console.log( "getDN ", score, "scores[score]", scores[score] );
			retvalDN = scores[score].DARTSNEEDED;
		}else{
			// console.log("scores.length !> 1");
			retvalDN = 9;
		}
	}else{
		retvalDN = 0;
	}
	return retvalDN;
}

function ndpClrs(dnDiff){
	let dnClrId = 0;
	switch(dnDiff){
		case -1:    dnClrId = 2;
					break;
		case 0:     dnClrId = 0;
					break;
		case 1:     dnClrId = 1;
					break;
		case 2:     dnClrId = 3;
					break;
	}
	return  clrArr[dnClrId]
}


function getNDPData(sb){
	console.log(
		"array stati:", 
		"scores", scores.length,
		"jsonSegs", jsonSegs.length,		
		"sb", sb
	);

	createDartBoard();

	ndpSegArray = [];
	
	let fnsb    =   sb;
	let sbdn    =   getDN(fnsb);
	// console.log("getNDPData: fnsb", fnsb, "sbdn", sbdn);

	for(let i=0; i < jsonSegs.length ;i++){
		let seg         = jsonSegs[i];
		//console.log("seg=\t", seg )
		if( seg.segMulti > 0 ){
			let thisSegSA   = (fnsb - seg.segVal); 
			let thisSegDN   = getDN( thisSegSA );
			let thisDNDiff  = (sbdn - thisSegDN); 
			let newColor 	= ( "fill: " + ndpClrs(thisDNDiff) + ";").toString()

			if( thisDNDiff !=0 ){
				d3.select("#"+ seg.segId )
					.attr("sb", 	fnsb 		)
					.attr("sa", 	thisSegSA 	)
					.attr("sbdn", 	sbdn 		)
					.attr("sadn", 	thisSegDN 	)
					.attr("sadndiff",thisDNDiff )
					.attr("style", newColor )
				;

				/*
					console.log(
						"checking dartboard (", seg.segId , 
						"segVal",               seg.segVal,     
						"thisSegSA",            thisSegSA,  
						"thisSegDN",            thisSegDN, 
						"thisDNDiff",           thisDNDiff,
						"arrEntry.NewColor:",            arrEntry.NewColor 
					);
				*/
			}else{
				d3.select("#"+ seg.segId ).attr("style","fill:#006400" );
			}
		}
	}
}
