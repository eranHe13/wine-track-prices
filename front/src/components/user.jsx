import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        // Attempt to get user data from sessionStorage on initial load
        const savedUserData = sessionStorage.getItem('user');
        return savedUserData ? JSON.parse(savedUserData) : {
            id: "",
            name: "",
            email: "",
            isLogged: false,
            products: []
        };
    });
    const updateUser = (userData) => {
        console.log("userData   - " , userData);
        setUser(prevUser => {
            const updatedUser = {
                ...prevUser, // Spread the previous user state to maintain other properties
                ...userData, // Spread the userData object to update the user state
                isLogged: true // Optionally set this based on some condition inside userData
            };
            // Save updated user data to sessionStorage
            sessionStorage.setItem('user', JSON.stringify(updatedUser));
            return updatedUser;
        });
    };

    useEffect(() => {
        console.log("User has been updated:", user);
    }, [user]); // Dependency array with 'user', so this runs every time 'user' changes

    

    return (
        <UserContext.Provider value={{ user, updateUser }}>
            {children}
        </UserContext.Provider>
    );
};



















const User  = {
    id:"",
    name : "",
    email : "",
    password : "",
    isLogged: false,
    products : {}
};


function getUser(){ 
    return User;

};

function updateUserLogin(bool){
    User.isLogged = bool;
}
function updateUser(id , name , email , password){
    User.id = id;
    User.name = name;
    User.email = email;
    User.password = password;
    User.isLogged = true;
}

function setUserData(data){
    const templateKeys = ['id', 'name', 'update_date', 'derech_hayin', 'paneco', 'haturky'];
    const map = new Map(data.map(item => {
        const obj = item.reduce((acc, currentValue, index) => {
            acc[templateKeys[index]] = currentValue;
            return acc;
        }, {});
        return [obj.id, obj];
    }));

    console.log(map);
    console.log("setUserData-- > " , data);
    User.products = map;    
}
export {User , getUser , updateUser , updateUserLogin , setUserData};








