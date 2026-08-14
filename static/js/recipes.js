
        // Modalni ochish va AI orqali ma'lumotlarni yuklash
        async function openRecipeModal(recipeId, title, ingredients) {
            const modal = document.getElementById('recipeModal');
            
            // Textlarni to'ldirish
            document.getElementById('modalTitle').innerText = title;
            document.getElementById('modalIngredients').innerText = ingredients;

            // Dastlab "yuklanmoqda" holatiga keltirish
            document.getElementById('modalCalories').innerText = "...";
            document.getElementById('modalProtein').innerText = "...";
            document.getElementById('modalCarbs').innerText = "...";
            document.getElementById('modalFat').innerText = "...";
            document.getElementById('modalFiber').innerText = "...";
            document.getElementById('benefitsBox').style.display = 'none';
            document.getElementById('modalBenefits').innerHTML = '';

            // Modalni ko'rsatish
            modal.style.display = 'flex';

            // Backendingizdagi AI API endpointiga so'rov yuborish
            try {
                const response = await fetch('/recipes/api/calculate-nutrition/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        recipe_id: recipeId,
                        ingredients: ingredients
                    })
                });

                if (!response.ok) {
                    throw new Error("Server xatosi");
                }

                const data = await response.json();

                // AI qaytargan ma'lumotlarni joy-joyiga qo'yish
                document.getElementById('modalCalories').innerText = data.calories || 0;
                document.getElementById('modalProtein').innerText = data.protein || '0g';
                document.getElementById('modalCarbs').innerText = data.carbs || '0g';
                document.getElementById('modalFat').innerText = data.fat || '0g';
                document.getElementById('modalFiber').innerText = data.fiber || '0g';

                const benefits = Array.isArray(data.benefits) ? data.benefits : [];
                const benefitsList = document.getElementById('modalBenefits');
                benefitsList.innerHTML = '';
                benefits.forEach(function (item) {
                    const li = document.createElement('li');
                    li.innerText = item;
                    benefitsList.appendChild(li);
                });
                document.getElementById('benefitsBox').style.display = benefits.length ? 'block' : 'none';

            } catch (error) {
                console.error("AI bilan bog'lanishda xatolik:", error);
                document.getElementById('modalCalories').innerText = "Xato";
                document.getElementById('modalProtein').innerText = "-";
                document.getElementById('modalCarbs').innerText = "-";
                document.getElementById('modalFat').innerText = "-";
                document.getElementById('modalFiber').innerText = "-";
                document.getElementById('benefitsBox').style.display = 'none';
            }
        }

        function getCookie(name) {
            const cookie = document.cookie.split('; ').find(row => row.startsWith(name + '='));
            return cookie ? decodeURIComponent(cookie.split('=').slice(1).join('=')) : '';
        }

        // Modalni yopish
        function closeRecipeModal() {
            document.getElementById('recipeModal').style.display = 'none';
        }

        // Modal tashqarisiga bosilganda yopilishi
        window.onclick = function(event) {
            const modal = document.getElementById('recipeModal');
            if (event.target === modal) {
                closeRecipeModal();
            }
        }
    