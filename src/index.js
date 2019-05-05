import React,{Component} from 'react'
import ReactDOM from 'react-dom'
import request from 'superagent'
import './style.css'
import Button from '@material-ui/core/Button';

import {OU,KIN,GIN,HISHA,KAKU,KEI,KYO,HU,RYU,UMA,NARIGIN,NARIKEI,NARIKYO,TOKIN} from './read'
import {OU_R,KIN_R,GIN_R,HISHA_R,KAKU_R,KEI_R,KYO_R,HU_R,RYU_R,UMA_R,NARIGIN_R,NARIKEI_R,NARIKYO_R,TOKIN_R} from './read'

const piece_images = [
    OU_R,KIN_R,GIN_R,HISHA_R,KAKU_R,KEI_R,KYO_R,HU_R,
    OU,KIN,GIN,HISHA,KAKU,KEI,KYO,HU,
    OU_R,KIN_R,NARIGIN_R,RYU_R,UMA_R,NARIKEI_R,NARIKYO_R,TOKIN_R,
    OU,KIN,NARIGIN,RYU,UMA,NARIKEI,NARIKYO,TOKIN,
]

class MainPage extends Component{

    constructor(props){
        super(props);
        this.status = {};
    }

    render(){
        return(
            <Board />
        );
    }
}

class Board extends Component{

    constructor(props){
        super(props);
        this.state = {
            "phase":0,
            "own":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "selected":{"x":null, "y":null, "own":null},
            "board":[[ 6,  5,  2,  1,  0,  1,  2,  5,  6],
                     [-1,  3, -1, -1, -1, -1, -1,  4, -1],
                     [ 7,  7,  7,  7,  7,  7,  7,  7,  7],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [15, 15, 15, 15, 15, 15, 15, 15, 15],
                     [-1, 12, -1, -1, -1, -1, -1, 11, -1],
                     [14, 13, 10,  9,  8,  9, 10, 13, 14]],
            "end":false
        };
    }

    
    action(e, row, col) {
        
        request
        .post('/action')
        .send({"row":row, "col":col})
        .end(
            (error, res) => {
                if (!error && res.status === 200) {
                    
                    var json_data = JSON.parse(res.text);
                    
                    
                    this.setState( json_data );

                } else {
                    console.log(error);
                }
            }
        );

    }

    clickButton(e,which){
        request
        .post('/power')
        .send({"power": which})
        .end(
            (error, res) => {
                if (!error && res.status === 200) {
                    
                    var json_data = JSON.parse(res.text);
                    
                    this.setState( json_data );

                } else {
                    console.log(error);
                }
            }
        );
    }

    clickOwn(e,what){
        request
        .post('/own')
        .send({"own": what})
        .end(
            (error, res) => {
                if (!error && res.status === 200) {
                    
                    var json_data = JSON.parse(res.text);
                    
                    this.setState( json_data );

                } else {
                    console.log(error);
                }
            }
        );
    }
        
    render() {
        
        if(this.state["end"]){
            alert("詰みです")
        }

        const Kinds = Array.apply(null, {length: 8}).map(Number.call, Number);
        const Rows = Array.apply(null, {length: 9}).map(Number.call, Number);

        return (
            <div id="Container">

                {(this.state.phase+1)%3===0?<Message clickButton={(e,which)=>{this.clickButton(e,which)}}/>:<div/>}

                <div id="battle_field">
                    
                    <table id="left_table">

                        {Kinds.map(
                            (i)=><tr key={i}><td 
                                onClick={(e)=>{this.clickOwn(e,i)}}
                                style={((this.state["phase"]-1)%3===0 && this.state.selected["own"]===i)?{"background-color":"red"}:{"background-color":"rgba(0,0,0,0)"}}
                            > {this.state["own"][i]===0?<div className="empty"/>:<img src={piece_images[i]}></img>} </td></tr>
                        )}
                        
                    </table>

                    <table id="main_table">
                        <TableRow row={this.state["board"][0]} nrow={0} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,0,col)}/>
                        <TableRow row={this.state["board"][1]} nrow={1} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,1,col)}/>
                        <TableRow row={this.state["board"][2]} nrow={2} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,2,col)}/>
                        <TableRow row={this.state["board"][3]} nrow={3} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,3,col)}/>
                        <TableRow row={this.state["board"][4]} nrow={4} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,4,col)}/>
                        <TableRow row={this.state["board"][5]} nrow={5} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,5,col)}/>
                        <TableRow row={this.state["board"][6]} nrow={6} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,6,col)}/>
                        <TableRow row={this.state["board"][7]} nrow={7} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,7,col)}/>
                        <TableRow row={this.state["board"][8]} nrow={8} phase={this.state["phase"]} selected={this.state["selected"]} action={(e,col)=>this.action(e,8,col)}/>
                    </table>

                    <table id="right_table">

                        {Kinds.map(
                            (i)=><tr key={i}><td 
                                onClick={(e)=>{this.clickOwn(e,i+8)}}
                                style={((this.state["phase"]-1)%3===0 && this.state.selected["own"]===i+8)?{"background-color":"red"}:{"background-color":"rgba(0,0,0,0)"}}
                            > {this.state["own"][i+8]===0?<div className="empty"/>:<img src={piece_images[i+8]}></img>} </td></tr>
                        )}

                    </table>
                    
                </div>
            </div>
        );
    }
}

const TableRow = (props)=>{

    const Cols = Array.apply(null, {length: 9}).map(Number.call, Number);
    
    return(
        <tr>
            {Cols.map(
                (col)=><td 
                    key={col} 
                    onClick={(e)=>props.action(e,col)}
                    style={((props.phase-1)%3===0 && props.nrow===props.selected["x"] && col===props.selected["y"])?{"background-color":"red"}:{"background-color":"rgba(0,0,0,0)"}}
                > {props.row[col]===-1?<div/>:<img src={piece_images[props.row[col]] }></img>} 
                </td>
            )}
        </tr>
    );
}

const Message = (props)=>{

    return(
        <div id="message_containor">
            <div id="question">
                成りますか？
            </div>

            <div id="buttons">

                <div id="yes">
                    <Button 
                        type="button" 
                        size='medium'
                        style={{fontSize:"20px", maxWidth: '100%', maxHeight: '100%', minWidth: '100%', minHeight: '100%'}}  
                        variant='contained' 
                        color='primary' 
                        onClick={(e)=>props.clickButton(e,"yes")}>
                        YES
                    </Button>
                </div>

                <div id="no">
                    <Button 
                        type="button" 
                        size='medium'
                        style={{fontSize:"20px", maxWidth: '100%', maxHeight: '100%', minWidth: '100%', minHeight: '100%'}}  
                        variant='contained' 
                        color='primary' 
                        onClick={(e)=>props.clickButton(e,"no")}>
                        NO
                    </Button>
                </div>
            </div>
        </div>
            
    );
}

ReactDOM.render(
    <MainPage />,
    document.getElementById('root')
);