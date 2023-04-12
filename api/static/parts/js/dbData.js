// db json as script in stead of 1423 lines of json
const segmentBase   =   [  "S",     "T",    "B",    "D",    "M" ];
const multis        =   [   1,      3,      1,      2,      0   ];
const segTexts      =   [ "Small single","Treble","Big single","Double","Missed"];
const numberBase    =   [ 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20 ];
const segRadPerc    =   [ 0.1200, 0.4900, 0.5900, 0.8100, 0.8900, 0.9999 ];
const radAngles     =   (idx,seg)=>{
                            nxtSeg = (parseInt(seg) + 1);
                            if(idx==0){ retObj = { "SA": 9, "EA": 27, "IR": segRadPerc[seg], "OR": segRadPerc[nxtSeg]};
                            }else if(idx==19){ retObj = { "SA": 351, "EA": 369, "IR": segRadPerc[seg], "OR": segRadPerc[nxtSeg]};
                            }else{ retObj = { "SA": ( ( idx * 18 ) + 9 ) , "EA":( ( idx * 18 ) + 27 ), "IR": segRadPerc[seg], "OR": segRadPerc[nxtSeg]  }; }
                            return retObj;
                        }
const colors        =   [   [ "#CBCBCB", "#000000"], // Small:      white / black
                            [ "#00FF00", "#FF0000"], // Triples:    green / red
                            [ "#CBCBCB", "#000000"], // Big:        white / black
                            [ "#00FF00", "#FF0000"], // Doubles:    green / red
                            [ "#585858", "#585858"], // Missed:     always same color
                            [ "#00FF00", "#FF0000"] // Bull:       green / red (not actually used )
                         ];
const nrToStr = (n)=>{ return ("0" + n.toString()).slice(-2); }

const dbjson = ()=>{
    let segArr = [];
    for(nr in numberBase){ /* console.log(nr, "creating segments for", numberBase[nr] ) */
        for(seg in segmentBase){
            let curSeg          =   {};
            let curRadAng       =   radAngles(nr, seg);
            curSeg.segId        =   segmentBase[seg] + nrToStr( numberBase[nr] );
		    curSeg.segGrp       =   numberBase[nr].toString();
		    curSeg.segMulti     =   multis[seg]; 
		    curSeg.segVal       =   multis[seg] * numberBase[nr] ;
		    curSeg.segSA        =   curRadAng.SA;
		    curSeg.segEA        =   curRadAng.EA;
		    curSeg.segInRad     =   curRadAng.IR;
		    curSeg.segOutRad    =   curRadAng.OR;
		    curSeg.segColor     =   nr%2===1? colors[seg][1]:colors[seg][0];
            curSeg.dbOrder      =   (parseInt(nr) + 1).toString() + (parseInt(seg) + 1).toString() - 10 ;
            curSeg.segTxt       =   segTexts[seg] + " " + numberBase[nr] + (seg==4? " outside":"" );    
            curSeg.segPath      =   "";
                segArr.push( curSeg );
        }
    }
    segArr.push(     /*  adding bulls. In the end adding them as fixed objects shortens and speeds up the code */
                { segId: "SBL",segGrp: "25",segMulti: 1,segVal: 25,segSA: 0,segEA: 360,segInRad: 0.0500, segOutRad: 0.1200,segColor: "#00FF00",dbOrder: 251,segTxt: "Single Bull",segPath: ""},
                { segId: "DBL",segGrp: "25",segMulti: 2,segVal: 50,segSA: 0,segEA: 360,segInRad: 0,segOutRad: 0.0500,segColor: "#FF0000",dbOrder: 252,segTxt: "Double Bull",segPath: ""}
    );
    return segArr;
}
//console.log("creating segmentArr", dbjson() );