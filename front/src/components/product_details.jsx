import React from 'react';
import LinkIcon from './assests/link.png'
const ProductDetails = ({ product }) => {
    const img = product.product_image ? product.product_image: null;
    const url = JSON.parse(product.details)
    
    
    const checkPrice = (price) =>{
      if(price === 0 ){
        return ""
      }
      return "₪" + price  
    }

    const sale = (sale_store) =>{
      const sp = JSON.parse(sale_store)
      if(sp.length === 0  || sp ===0){
        return ""
      }
      else{
        sp[2] = sp[2].toFixed(2)
        return(`${sp[0]} ב- ${sp[1]} --> ${sp[2]}`) 
        }
      }
    

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%' }}>
      
      {/* Product Name in the Center */}
      
      
      <div style={{ display: 'flex', justifyContent: 'space-around'   }}>
      
        {/* Product Details on the Left */}
       <div style={{ padding: '30px 25px'}}>
       <h2 class="display-1" style={{ textAlign: 'center' }}>{product.name}</h2>
      <h3 style={{ textAlign: 'center' , padding:"20px" }}>המחיר שלי : ₪{product.desire_price}</h3>
        <table class="table" style={{ padding: '0 5px', direction: 'rtl' , fontSize:"25px" }}>
          <thead>
            <tr>
              <th scope="col"> <strong> קישור </strong> </th>
              <th scope="col"><strong>חנות</strong></th>
              <th scope="col"><strong>מחיר רגיל</strong></th>
              <th scope="col"><strong>מחיר מועדון</strong></th>
              <th scope="col"><strong>מחיר סייל</strong></th>
              
            </tr>
          </thead>
          <tbody>
            <tr>
            <th scope="row">
              <a href={url["derech_hyin"]}>
                <img src={LinkIcon} style={{
                  cursor: 'pointer',
                  height: '25px', 
                  width: '25px',
                  objectFit: 'cover'}}/>
              </a>
              </th>
              <td>דרך היין</td>
              <td>{checkPrice(product.rp_derech)}</td>
              <td>{checkPrice(product.cp_derech)}</td>
              <td>{sale(product.sp_derech)}</td>
            </tr>
            <tr>
            <th scope="row"><a href={url["paneco"]}><img src={LinkIcon} style={{
                  cursor: 'pointer',
                  height: '25px', 
                  width: '25px',
                  objectFit: 'cover'}}/>
                  </a></th>
              <td>פנקו</td>
              <td>{checkPrice(product.rp_paneco)}</td>
              <td>{checkPrice(product.cp_paneco)}</td>
              <td>{sale(product.sp_paneco)}</td>
            </tr>
            <tr>
            <th scope="row"><a href={url["haturki"]}><img src={LinkIcon} style={{
                  cursor: 'pointer',
                  height: '25px', 
                  width: '25px',
                  objectFit: 'cover'}}/>
                  </a></th>
              <td>הטורקי</td>
              <td>{checkPrice(product.rp_haturkey)  }</td>
              <td>{checkPrice(product.cp_haturkey)}</td>
              <td>{sale(product.sp_haturkey) }</td>            </tr>
            {/* Additional product details can be dynamically inserted here */}
          </tbody>
        </table>
        </div>
        <div >

        {/* Product Image and Description on the Right */}
        <div  style={{  textAlign: 'center', padding: '0 20px'  }}>
          <img class="card-img-top" src={img} alt={product.name} style={{height:"600px"}} />
          <p class="card-text" ></p>
          <p class="card-text"><small class="text-body-secondary">Last updated this morning</small></p>
        </div>
      </div>
      </div>
    </div>
  );
};

export default ProductDetails;

// <div style={{ flex: 1, padding: '0 20px', direction: 'rtl' }}>
//           <p>דרך היין : {product.derech_hayin}</p>
//           <p>פנקו : {product.paneco}</p>
//           <p>הטורקי : {product.haturkey}</p>
//           {/* Additional product details can go here */}
//         </div>
