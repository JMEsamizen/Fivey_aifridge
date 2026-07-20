document.addEventListener(
    "DOMContentLoaded",
    function(){
        const buttons =
        document.querySelectorAll(
            ".hero-buttons a, .nav-signup"
        );
        buttons.forEach(button=>{

            button.addEventListener(
                "mouseenter",
                ()=>{
                    button.style.transform =
                    "translateY(-3px)";
                }
            );

            button.addEventListener(
                "mouseleave",
                ()=>{
                    button.style.transform =
                    "translateY(0)";
                }
            );

        });

        const cards =
        document.querySelectorAll(
            ".feature"
        );

        cards.forEach((card,index)=>{
            card.style.opacity="0";
            card.style.transform="translateY(30px)";
            setTimeout(()=>{
                card.style.transition=
                "0.6s ease";
                card.style.opacity="1";
                card.style.transform=
                "translateY(0)";
            }, index*200);
        });
});