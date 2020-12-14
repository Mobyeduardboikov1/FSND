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


const Movies = () => {
    
    const { getAccessTokenSilently } = useAuth0();
    const [state, setState] = useState({
        showResult: false,
        apiMessage: "",
        error: null,
        showMovieForm: false,
        movie_title: '',
        movie_release_date: '',
        movie_id: null,
        movieList: [],
        token: null,
        fetchedMovies: false,

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
        axios.post(`${apiHost}/movies`, {
            title: state.movie_title,
            release_date: state.movie_release_date,
        }).then(response => {
                 console.log('movies list > ', response.data);
                 setState({
                    ...state, 
                    showMovieForm: false,
                    movie_title: '',
                    movie_release_date: '',
                    movie_id: null,
                 })
             }).then(() => { getMovieList(); });

    }
    
    const handleUpdate = ({ title, release_date, id }) => {
        axios.patch(`${apiHost}/movies/${id}`, {
            title,
            release_date
        }).then(response => {
                 console.log('movies list > ', response.data);
                 setState({
                    ...state,
                    showMovieForm: false,
                    movie_release_date: '',
                    movie_title: '',
                    movie_id: null,
                    isUpdate: false            
                 })
        }).then(() => {getMovieList(); });

    }

    const handleDelete = (id) => {
        axios.delete(`${apiHost}/movies/${id}`).then(response => {
                 console.log('movies list > ', response.data);
                 setState({
                    ...state,
                    showMovieForm: false                 
                 })
             },{
                headers: {
                  Authorization: 'Bearer ' + state.token
                }
              }).then(() => {getMovieList(); });
    }

    const can = (permission) => {
        if (state.decodedToken.permissions.includes(permission)) {
            return true;
        }

        return false;
    }
    const getMovieList = () => {
        axios.get(`${apiHost}/movies`).then(response => {
            setState({ ...state, movieList: response.data.movies, fetchedMovies: true });
        })
    };

    if (state.token && !state.fetchedMovies) {
        getMovieList();
    } 

    if (!state.token) {
        console.log('state ', state);
        return null;
    }
    return (
        <div>
            {can('add:movie') && (
            <div>
                <Button
                    onClick={() => { setState({ ...state, showMovieForm: true })}}
                    className="btn-margin"
                    color="primary"
                >
                New Movie
                </Button>
                
            </div>
            )}
            {state.showMovieForm && (
                <div>
                    <div>
                        <Label for="movie_title">Title</Label>
                        <Input 
                            value={state.movie_title}
                            onChange={(e) => { setState({ ...state, movie_title:  e.target.value}); }} type="text" id="movie_title"></Input>      
                    </div>
                    <div>
                        <Label for="movie_release_date">Release Date (YYYY-MM-DD)</Label>
                        <Input 
                            value={state.movie_release_date}
                            onChange={(e) => { console.log(e, this); setState({ ...state, movie_release_date:  e.target.value}); }} type="text" id="movie_release_date"></Input>      
                    </div>
                    <Button onClick={(e) => { 
                        if (state.isUpdate) {
                            handleUpdate({ title: state.movie_title, age: state.movie_release_date, id: state.movie_id });
                            return;
                        } 
                        handleSubmit();
                    }}>Submit</Button>
                    <Button onClick={(e) => { setState({ showMovieForm: false })}}>Close</Button>
                </div>
            )}
            <div id="movie-list">
                {state.movieList && state.movieList.map(movie => {
                    return (
                        <div className="movie-entry">
                            <h4>Movie List</h4>
                            <span>{movie.title}</span>
                            <span>{movie.release_date}</span>
                            <div>
                                {can('update:movie') && (
                                    <Button onClick={(e) => {
                                    setState({ showMovieForm: true, isUpdate: true, movie_title: movie.title, movie_release_date: movie.release_date, movie_id: movie.id });
                                
                                }}>
                                Edit
                                </Button>
                                )}
                                {can('delete:movie') && <Button onClick={(e) => { handleDelete(movie.id); }}>Delete</Button>}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Movies;