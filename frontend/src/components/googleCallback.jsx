import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { login } from "../redux/accessSlice";
import { toast } from "react-hot-toast";

const GoogleCallback = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const hasHandled = useRef(false); // Guard to ensure effect runs only once

  useEffect(() => {
    if (hasHandled.current) return; // Exit if already run
    hasHandled.current = true;

    const params = new URLSearchParams(window.location.search);
    const access = params.get("access");
    const refresh = params.get("refresh");

    if (access && refresh) {
      // Store tokens in localStorage
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
      dispatch(login());
      toast.success("Login successful!");
      navigate("/"); // Redirect to home
    } else {
      console.log("eta po ayo");
      navigate("/login"); // Redirect to login if tokens are missing
    }
  }, []);

  return <div>Redirecting...</div>;
};

export default GoogleCallback;
