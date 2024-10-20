import { useContext, createContext, useState, ReactNode } from 'react'
import * as React from 'react'
import { useNavigate } from 'react-router-dom'

//Create element that can be read by the rest of the webapp
const AuthContext = createContext<AuthContextType | undefined>(undefined);

//Interface for login Credentials
interface userCredentials {
    username: string,
    password: string
}
//Interface to wrap components within the app
interface authProps {
    children: ReactNode;
}
//Interface to define values exported from AuthProvider
interface AuthContextType {
    adminInitials: string | null,
    token: string | null,
    attemptLogin: (data: userCredentials) => Promise<void | string>,
    logOut: () => void;
}

//This handles the login/logout of the webpapp
const AuthProvider: React.FC<authProps> = ({children}) => {
    const [adminInitials, setAdminInitials] = useState("");                 //Admin Initials -> for Assigning to comments
    const [token, setToken] = useState(localStorage.getItem("token") || ""); //Site Token, the meat of authentication.
    const navigate = useNavigate();
    //This calls to the backend to attempt to login, on success it returns the adminInitials and a token for site authentication.
    const attemptLogin = async (data: userCredentials) => {
        const loginDetails = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                UserName: data.username,
                Password: data.password
            })
        }
        try{
            const login = await fetch(`/api/login`,loginDetails)
            const data = await login.json()
            console.log(data)
            if(data.Success == true){
                setAdminInitials(data.adminInitials)
                setToken(data.userToken);
                localStorage.setItem('token',data.userToken)
                navigate('/events')
                return;
            } else {
                console.error("Error on User Login", data)
                return data.Message
            }
        }catch(e: any){
            console.error("Error on User Login",e)
            if (e.response && e.response.data && e.response.data.Success) {
                return e.response.data.Success; // Return error message from backend
            }
        }
    };
    const logOut = () => {
        setAdminInitials("");
        setToken("")
        localStorage.removeItem('token')
        navigate('/login')
    };

    return (
        <AuthContext.Provider value={{adminInitials, token, attemptLogin, logOut}}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;

export const useAuth = () => {
    return useContext(AuthContext);
};