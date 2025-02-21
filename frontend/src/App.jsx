
import { Route, Routes } from 'react-router-dom'
import Login from './pages/login'
import Signup from './pages/signup'
import { useSelector } from "react-redux";
import ProtectedRoute from './redux/protectedRoute'
import  UserAuthForm  from './pages/signup'
import UserRegister from './pages/userRegister'
import GoogleCallback from './components/googleCallback'
import { Index } from './pages';
import ForgotPassword from './pages/forgotPassword';
import ResetPassword from './pages/resetPassword';
import HeaderBlog from './components/Blogs/blogHeader';
import BlogsView from './components/Blogs/blogs';
import SingleBlog from './components/Blogs/singleblog';
import CategoryBlog from './components/Blogs/catblog';
import BlogPost from './components/Blogs/BlogPost';
function App() {
  const { isAuthenticated } = useSelector((state) => state.root);
  return (
   <Routes>
    <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />}>
      <Route path = '/' element = {<Index/>}/>
    </Route>
    <Route path="/login" element={<Login/>}/>
    <Route path="/google/callback" element={<GoogleCallback />} />
    <Route path="/signup" element={<UserAuthForm/>}/>
    <Route path='/register' element={<UserRegister/>}/>
    <Route path='/forgot-password' element = {<ForgotPassword/>}/>
    <Route path='/reset-password/:uid/:token' element = {<ResetPassword/>}/>

    <Route path="/blog" element={<HeaderBlog />}>
          <Route path="" element={<BlogsView />} />
          <Route path=":id" element={<SingleBlog />} />
          <Route path="cat/:cat" element={<CategoryBlog />} />
          <Route path="post" element={<BlogPost />} />
        </Route>

    
      </Routes>
  )
}

export default App
