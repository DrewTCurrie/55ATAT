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
    attemptLogin: (data: userCredentials) => Promise<void>,
    logOut: () => void;
}

//This handles the login/logout of the webpapp
const AuthProvider: React.FC<authProps> = ({children}) => {
    const [adminInitials, setAdminInitials] = useState("");                 //Admin Initials -> for Assigning to comments
    const [token, setToken] = useState(localStorage.getItem("site") || ""); //Site Token, the meat of authentication.
    const navigate = useNavigate();
    //This calls to the backend to attempt to login, on success it returns the adminInitials and a token for site authentication.
    const attemptLogin = async (data: userCredentials) => {

    };
    const logOut = () => {
        setAdminInitials("");
        setToken("")
        localStorage.removeItem('site')
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