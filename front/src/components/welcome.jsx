import React from "react";
import Welcome_img from "./assests/welcome_img.png"
const Welcome = () =>{
    return(
        <div class="display-1" style={{textAlign: 'center'}}>
        <h1>ברוכים הבאים </h1>
        <h2>שמחים שהצטרפתם אלינו , אתם תבחרו יין ומחיר שאותו אתם מוכנים לשלם </h2>
        <h2>ואנחנו נציג לכם את כל המחירים מהאתרים איתם אנחנו עובדים </h2>
        <h2>בנוסף ברגע שתיהיה התאמה בין מחיר היין שלכם למחיר מהחנויות אנחנו נתריע אליכם באמצעות אימייל </h2>
        <img src={Welcome_img} style={{
                  padding: "20px",
                  height: '600px', 
                  width: '1000px',
                  objectFit: 'cover'}}/>

        </div>
        
    )
}
export default Welcome


