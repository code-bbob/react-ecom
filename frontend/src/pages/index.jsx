import React from 'react';
import { useDispatch } from "react-redux";
import { login, logout } from "../redux/accessSlice";
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import useAxios from '../utils/useAxios';


export const Index = () => {

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const api = useAxios();
  const handleLogout = (e) => {
    // Remove tokens from local storage
    e.preventDefault()
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    dispatch(logout());

    // Redirect or navigate to the login page
    // For example, redirect to the login page
    // history.push('/login');
  };


  const handleClick = () => {
    console.log("hererere")
    const res = api.get("api/auth/google/")
  }
  
  return (
    <div><Button onClick={(e)=>handleLogout(e)}>Logout</Button>
    <Button onClick={()=>handleClick()}>bla</Button>
    </div>

  )
}
