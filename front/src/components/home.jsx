import React, {   useState, useEffect }  from "react";
import { FaWineBottle , FaTrash  } from "react-icons/fa";
import {useUser} from "./user";
import AddProductForm from "./add_Wine_Form";
import ProductDetails from "./product_details"
import { removeWine } from "../server";
import { useNavigate } from 'react-router-dom';
import logo from "./assests/logo.jpg";
import logoutLogo from "./assests/logout.png";
import Welcome from "./welcome";

function Home(props) {
  const { user , updateUser  } = useUser();
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAddProduct, setShowAddProduct] = useState(false);
  const navigate = useNavigate(); // Initialize useNavigate hook


  if(!user.isLogged){
    navigate("/");
  }



  useEffect(() => {
    if (user.products && typeof user.products === 'string') {
      console.log("Parsing user.products as JSON");
      const productsArray = JSON.parse(user.products);
      const productsWithKeys = productsArray.map(([key, obj]) => ({
        ...obj,
        key // Adding the key from the array to the object
      }));
      setProducts(productsWithKeys);
    } else if (user.products && typeof user.products === 'object') {
      console.log("Using user.products as object");
      // Assuming user.products is an object where keys are product ids and values are product objects
      const productsWithKeys = Object.entries(user.products).map(([key, obj]) => ({
        ...obj,
        key // Adding the key from the object to the product
      }));
      setProducts(productsWithKeys);
    }
    console.log("products--->", products);
  }, [user.products]); // Add user.products as a dependency
  
  
  const handleAddProductClick = () => {
    setShowAddProduct(true);
    setSelectedProduct(null); // Deselect any selected product
  };

  
  const handleProductClick = (product) => {
    setShowAddProduct(null);
    setSelectedProduct(product);
    
  };

  const handleLogOut = () => {
    sessionStorage.clear();
    navigate("/");
  }

  const handleDeleteProduct = async (key) => {
    // Find the product with the matching key
    const chosenProduct = products.find(product => product.key === key);
    // Log key and chosen product ID for debugging
    console.log("key:", key, "chosenProduct:", chosenProduct.id);
    // Update state to remove the product
    setProducts(products.filter(product => product.key !== key));
    // Log user ID and product ID being removed
    console.log("user id --", user.id, "product-id--:", key);
    // Perform the removeWine operation and update the user
    const res = await removeWine({"user_id": user.id, "product_id": chosenProduct.id}, updateUser);
    // Deselect any selected product
    setSelectedProduct(null);
    // Update the user's products after deletion
    await updateUser({products: products.filter(product => product.key !== key)});
    // Log a message indicating the operation's completion
    console.log("Operation completed for user id --", user.id);
  };



  if (isLoading) return <p>Loading products...</p>;
  if (error) return <p>Error fetching products: {error}</p>;

 
  return (
    <div >
   <div className="header" style={{
    display: 'flex', 
    flexDirection: 'row', 
    alignItems: 'center',  // Ensure items are vertically centered
    height: "190px", 
    margin: "15px",
    justifyContent: 'space-between' ,// Distribute space evenly between the items
    borderBottom: '1px solid #ccc',
    backgroundColor : "#E1E5DC"
}}>
  {/* Logo on the left with a circular radius */}
  <img src={logo} alt="Logo" style={{
    height: '150px', // Adjust based on your preference
    width: '150px',  // Making the width equal to the height for a circle
    borderRadius: '50%',  // Circular radius
    objectFit: 'cover', // Cover to ensure the image fully fills the circle
    marginLeft:"15px"
  }} />
  
  {/* User name in the middle */}
  <span style={{
    flex: 1, 
    textAlign: 'center',  // Center the text
    fontSize: '54px',  // Adjust font size as needed
    fontStyle:"italic"
  }}>
    {user.name}
  </span>
  
  {/* Logout button on the right */}
  
    <img src={logoutLogo} style={
      { cursor: 'pointer',
        height: '60px', // Adjust based on your preference
        width: '60px',  // Making the width equal to the height for a circle
        borderRadius: '50%',  // Circular radius
        objectFit: 'cover', // Cover to ensure the image fully fills the circle
        marginRight:"35px"
}
    } onClick={handleLogOut}></img>
  
</div>

    <div className="" style={{ display: 'flex', flexDirection: 'row', height: '100vh' }}>
    <div className="listproducts" style={{ flex: '1', overflowY: 'auto', borderLeft: '2px solid #ccc' ,order:"1"}}>
      <div class="d-flex justify-content-center"  >
    <button class="btn btn-primary" onClick={handleAddProductClick } style={{marginTop:"20px" ,width:"80%" , fontSize:"20px" }}>הוסף יין</button>
    </div>
    <div class="d-flex justify-content-center"  >
      <ul style={{ listStyleType: 'none', paddingLeft: "15px" , paddingTop:"15px"  , fontSize:"27px" ,  direction:"rtl"}}>
        {products.map((product) => (
          <li key={product.key} style={{ padding: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}>
          <span onClick={() => handleProductClick(product)}>{product.name}</span>
          <FaTrash onClick={() => handleDeleteProduct(product.key)} style={{ cursor: 'pointer' ,width:"17px" , height:"17px" , marginRight:"15px"}}/>
        </li>
        ))}
      </ul>
      </div>
    </div>
    <div className="productDetails" style={{ alignItems:"center" ,  flex: '4', padding: '20px',order:"-1" }}>
    {showAddProduct ? (
          <AddProductForm user={user} updateUser={updateUser} />

        ) : selectedProduct ? (
          <ProductDetails product={selectedProduct} />
        ) : (
          <Welcome />   
)}    </div>
  </div>
  </div>
 
  );
}

export default Home;



