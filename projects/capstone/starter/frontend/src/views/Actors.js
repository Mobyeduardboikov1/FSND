import React, { useEffect, useState } from "react";
import axios from 'axios';
import config from '../config.json';
import {
    Button,
    Label,
    Input
  } from "reactstrap";
import { useAuth0 } from "@auth0/auth0-react";
import jwt_decode from "jwt-decode";
// styles
import "./../App.css";
const { apiHost } = config;


const Actors = () => {
    
    const { getAccessTokenSilently } = useAuth0();
    const [state, setState] = useState({
        showResult: false,
        apiMessage: "",
        error: null,
        showActorForm: false,
        actor_name: '',
        actor_age: '',
        actor_gender: '',
        actor_id: null,
        actorList: [],
        token: null,
        fetchedActors: false,

    });
    
    const getToken = async () => {
        const token = await getAccessTokenSilently();
        console.log('got token ', token);
        setState({ ...state, token: token, decodedToken: jwt_decode(token) });
    };

    if (!state.token) { 
        console.log('getting token, ', state.token);
        getToken();
    }
    console.log('state > ', state);

    axios.defaults.baseURL = apiHost;
    
    axios.defaults.headers.common['Content-Type'] ='application/json;charset=utf-8';
    axios.defaults.headers.get['Access-Control-Allow-Origin'] = '*';
    axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
    axios.defaults.headers.patch['Access-Control-Allow-Origin'] = '*';
    axios.defaults.headers.get['Access-Control-Allow-Origin'] = '*';
    axios.defaults.headers.get['Authorization'] = 'Bearer ' + state.token;
    axios.defaults.headers.post['Authorization'] = 'Bearer ' + state.token;
    axios.defaults.headers.patch['Authorization'] = 'Bearer ' + state.token;
    axios.defaults.headers.delete['Authorization'] = 'Bearer ' + state.token;

    console.log('axios default hedaers ', axios.defaults);


    const handleSubmit = () => {
        console.log('сonfig > ', config, 'apiServer',apiHost);
        axios.post(`${apiHost}/actors`, {
            name: state.actor_name,
            age: state.actor_age,
            gender: state.actor_gender,
        }).then(response => {
                 console.log('actors list > ', response.data);
                 setState({
                    ...state, 
                    showActorForm: false,
                    actor_name: '',
                    actor_age: '',
                    actor_gender: '',
                    actor_id: null,
                 })
             });

    }
    
    const handleUpdate = ({ name, age, gender, id }) => {
        console.log('name > ', name, id, age, gender);
        axios.patch(`${apiHost}/actors/${id}`, {
            name,
            age,
            gender
        }).then(response => {
                 console.log('actors list > ', response.data);
                 setState({
                    ...state,
                    showActorForm: false,
                    actor_age: '',
                    actor_name: '',
                    actor_gender: '',
                    actor_id: null,
                    isUpdate: false            
                 })
        }).then(() => {getActorList(); });

    }

    const handleDelete = (id) => {
        axios.delete(`${apiHost}/actors/${id}`).then(response => {
                 console.log('actors list > ', response.data);
                 setState({
                    ...state,
                    showActorForm: false                 
                 })
             },{
                headers: {
                  Authorization: 'Bearer ' + state.token
                }
              }).then(() => {getActorList(); });
    }

    const can = (permission) => {
        if (state.decodedToken.permissions.includes(permission)) {
            return true;
        }

        return false;
    }
    const getActorList = () => {
        axios.get(`${apiHost}/actors`).then(response => {
            setState({ ...state, actorList: response.data.actors, fetchedActors: true });
        })
    };

    if (state.token && !state.fetchedActors) {
        getActorList();
    } 

    if (!state.token) {
        console.log('state ', state);
        return null;
    }
    return (
        <div>
            {can('add:actor') && (
            <div>
                <Button
                    onClick={() => { setState({ ...state, showActorForm: true })}}
                    className="btn-margin"
                    color="primary"
                >
                New Actor
                </Button>
                
            </div>
            )}
            {state.showActorForm && (
                <div>
                    <div>
                        <Label for="actor_name">Name</Label>
                        <Input 
                            value={state.actor_name}
                            onChange={(e) => { setState({ ...state, actor_name:  e.target.value}); }} type="text" id="actor_name"></Input>      
                    </div>
                    <div>
                        <Label for="actor_age">Age</Label>
                        <Input 
                            value={state.actor_age}
                            onChange={(e) => { console.log(e, this); setState({ ...state, actor_age:  e.target.value}); }} type="text" id="actor_age"></Input>      
                    </div>
                    <Input 
                        value={state.actor_gender}
                        onChange={(e) => { setState({ ...state, actor_gender:  e.target.value}); }} type="select" id="actor_gender">
                        <option value="">Select a value</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </Input>
                    <Button onClick={(e) => { 
                        if (state.isUpdate) {
                            handleUpdate({ name: state.actor_name, age: state.actor_age, gender: state.actor_gender, id: state.actor_id });
                            return;
                        } 
                        handleSubmit();
                    }}>Submit</Button>
                    <Button onClick={(e) => { setState({ showActorForm: false })}}>Close</Button>
                </div>
            )}
            <div id="actor-list">
                {state.actorList && state.actorList.map(actor => {
                    return (
                        <div className="actor-entry">
                            <h4>Actor List</h4>
                            <span>{actor.name}</span>
                            <span>{actor.gender}</span>
                            <span>{actor.age}</span>
                            <div>
                                {can('update:actor') && (
                                    <Button onClick={(e) => {
                                    setState({ showActorForm: true, isUpdate: true, actor_name: actor.name, actor_age: actor.age, actor_gender: actor.gender, actor_id: actor.id });
                                
                                }}>
                                Edit
                                </Button>
                                )}
                                {can('delete:actor') && <Button onClick={(e) => { handleDelete(actor.id); }}>Delete</Button>}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Actors;