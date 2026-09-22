let cart = JSON.parse(localStorage.getItem("lunashid_cart") || "[]");

function addToCart(id,name,price){
    cart.push({id:id,name:name,price:price});
    localStorage.setItem("lunashid_cart",JSON.stringify(cart));
    alert("محصول به سبد اضافه شد.");
}

function renderCart(){

    const box=document.getElementById("cartItems");
    const total=document.getElementById("cartTotal");

    if(!box || !total) return;

    if(cart.length===0){
        box.innerHTML="<div class='empty glass'>سبد خرید خالی است.</div>";
        total.textContent="0 تومان";
        return;
    }

    let sum=0;

    box.innerHTML=cart.map((item,index)=>{

        sum += Number(item.price);

        return `
        <div class="glass"
             style="padding:18px;margin:10px 0;border-radius:18px;display:flex;justify-content:space-between">
            <span>${item.name}</span>
            <span>${Number(item.price).toLocaleString()} تومان</span>
            <button onclick="removeCart(${index})">×</button>
        </div>
        `;

    }).join("");

    total.textContent=sum.toLocaleString()+" تومان";
}

function removeCart(index){
    cart.splice(index,1);
    localStorage.setItem("lunashid_cart",JSON.stringify(cart));
    renderCart();
}

function checkout(){

    if(cart.length===0){
        alert("سبد خرید خالی است.");
        return;
    }

    const total=cart.reduce((a,b)=>a+Number(b.price),0);

    fetch("/api/order",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            items:JSON.stringify(cart),
            total:total
        })
    })
    .then(r=>r.json())
    .then(()=>{
        alert("سفارش شما ثبت شد.");
        cart=[];
        localStorage.removeItem("lunashid_cart");
        renderCart();
    });
}

renderCart();
