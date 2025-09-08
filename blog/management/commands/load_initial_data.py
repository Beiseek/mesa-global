from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from blog.models import Region, Category, Tag, Recipe, Article
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Load initial data for Mesa Global blog'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        
        # Create regions
        regions_data = [
            {'name': 'Mexico', 'slug': 'mexico', 'description': 'Rich culinary traditions from ancient Aztec and Maya civilizations combined with Spanish influences.'},
            {'name': 'Italy', 'slug': 'italy', 'description': 'Mediterranean cuisine featuring fresh ingredients, pasta, and regional specialties.'},
            {'name': 'India', 'slug': 'india', 'description': 'Diverse spices and cooking techniques vary dramatically across different regions.'},
            {'name': 'Thailand', 'slug': 'thailand', 'description': 'Balance of sweet, sour, salty, and spicy flavors in every dish.'},
            {'name': 'France', 'slug': 'france', 'description': 'Sophisticated culinary techniques and emphasis on quality ingredients.'},
        ]
        
        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                slug=region_data['slug'],
                defaults=region_data
            )
            if created:
                self.stdout.write(f'Created region: {region.name}')
        
        # Create categories
        categories_data = [
            {'name': 'Main Dishes', 'slug': 'main-dishes', 'description': 'Hearty main courses and entrees'},
            {'name': 'Appetizers', 'slug': 'appetizers', 'description': 'Small plates and starters'},
            {'name': 'Desserts', 'slug': 'desserts', 'description': 'Sweet treats and traditional desserts'},
            {'name': 'Soups', 'slug': 'soups', 'description': 'Comforting soups and broths'},
            {'name': 'Street Food', 'slug': 'street-food', 'description': 'Popular street food and snacks'},
        ]
        
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=category_data['slug'],
                defaults=category_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create tags
        tags_data = [
            'Spicy', 'Vegetarian', 'Traditional', 'Quick', 'Family Recipe',
            'Festival Food', 'Comfort Food', 'Healthy', 'Ancient Recipe'
        ]
        
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
        
        # Create recipes
        self.create_recipes()
        
        # Create articles
        self.create_articles()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data!'))
    
    def download_image(self, url, filename):
        """Download image from URL and return ContentFile"""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return ContentFile(response.content, filename)
        except:
            pass
        return None
    
    def create_recipes(self):
        """Create 5 authentic recipes"""
        mexico = Region.objects.get(slug='mexico')
        italy = Region.objects.get(slug='italy')
        india = Region.objects.get(slug='india')
        thailand = Region.objects.get(slug='thailand')
        france = Region.objects.get(slug='france')
        
        main_dishes = Category.objects.get(slug='main-dishes')
        appetizers = Category.objects.get(slug='appetizers')
        soups = Category.objects.get(slug='soups')
        
        recipes_data = [
            {
                'title': 'Traditional Mole Poblano',
                'slug': 'traditional-mole-poblano',
                'region': mexico,
                'category': main_dishes,
                'description': 'A complex, rich sauce with over 20 ingredients including chocolate, served traditionally with turkey or chicken.',
                'history': '''<p>Mole Poblano is perhaps Mexico's most celebrated dish, with origins dating back to the 17th century in the Convent of Santa Rosa in Puebla. Legend tells of Sister Andrea de la Asunción, who created this complex sauce to honor a visiting bishop.</p>
                
                <p>The dish represents the perfect fusion of indigenous Mexican ingredients like chocolate, chili peppers, and tomatoes with Spanish influences such as almonds, raisins, and spices brought from Europe and Asia.</p>
                
                <p>Today, mole remains a centerpiece of Mexican celebrations, particularly during Day of the Dead festivities and weddings, taking hours to prepare and representing the love and dedication of the cook.</p>''',
                'cultural_context': '''<p>Mole Poblano is deeply embedded in Mexican culture as a symbol of hospitality and celebration. Families often have their own secret recipes passed down through generations, with each cook adding their personal touch.</p>
                
                <p>The preparation of mole is often a communal activity, bringing together multiple generations of women who share stories while grinding spices and stirring the pot. This tradition reinforces family bonds and cultural identity.</p>
                
                <p>During the Day of the Dead, mole is prepared as an offering to deceased loved ones, representing the continuation of family traditions beyond death.</p>''',
                'ingredients': '''<ul>
                    <li>6 dried mulato chiles, stemmed and seeded</li>
                    <li>4 dried ancho chiles, stemmed and seeded</li>
                    <li>2 dried chipotle chiles, stemmed and seeded</li>
                    <li>2 Roma tomatoes</li>
                    <li>1 white onion, quartered</li>
                    <li>4 garlic cloves</li>
                    <li>1/4 cup sesame seeds</li>
                    <li>2 tablespoons pumpkin seeds</li>
                    <li>1/4 cup raisins</li>
                    <li>2 tablespoons lard or vegetable oil</li>
                    <li>1 corn tortilla, torn into pieces</li>
                    <li>2 ounces Mexican chocolate, chopped</li>
                    <li>1 teaspoon ground cinnamon</li>
                    <li>1/2 teaspoon ground cloves</li>
                    <li>1/2 teaspoon anise seeds</li>
                    <li>1 bay leaf</li>
                    <li>Salt to taste</li>
                    <li>2-3 cups chicken or turkey broth</li>
                </ul>''',
                'instructions': '''<ol>
                    <li><strong>Prepare the chiles:</strong> Heat a dry skillet over medium heat. Toast the chiles for 2-3 minutes until fragrant, being careful not to burn them. Place in a bowl and cover with hot water. Let soak for 30 minutes.</li>
                    
                    <li><strong>Char the vegetables:</strong> Char the tomatoes, onion, and garlic directly over an open flame or in a dry skillet until blackened in spots. Set aside to cool.</li>
                    
                    <li><strong>Toast the seeds and spices:</strong> In the same dry skillet, toast sesame seeds until golden, then pumpkin seeds until they puff up. Toast the cinnamon, cloves, anise, and bay leaf for 30 seconds until fragrant.</li>
                    
                    <li><strong>Fry the tortilla:</strong> Heat lard in a large pot over medium heat. Fry the torn tortilla until crispy and golden. Remove and drain.</li>
                    
                    <li><strong>Blend the mole:</strong> Drain the chiles and blend with charred vegetables, toasted seeds and spices, fried tortilla, raisins, and 1 cup of broth until smooth. Strain through a fine-mesh sieve.</li>
                    
                    <li><strong>Cook the mole:</strong> Heat the remaining lard in the pot. Add the mole paste and cook, stirring constantly, for 20-30 minutes until darkened and fragrant. Add chocolate and remaining broth gradually until desired consistency is reached.</li>
                    
                    <li><strong>Season and serve:</strong> Season with salt and simmer for another 10 minutes. Serve over turkey or chicken with warm tortillas.</li>
                </ol>''',
                'prep_time': 60,
                'cook_time': 120,
                'servings': 8,
                'difficulty': 'hard',
                'image_url': 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'Authentic Risotto alla Milanese',
                'slug': 'authentic-risotto-alla-milanese',
                'region': italy,
                'category': main_dishes,
                'description': 'Creamy saffron risotto from Milan, the golden jewel of Northern Italian cuisine.',
                'history': '''<p>Risotto alla Milanese dates back to the 16th century and is inextricably linked to the construction of the Duomo di Milano. Legend attributes its creation to Valerius of Flanders, a young assistant to Benedetto da Norcia, the master glazier working on the cathedral's stained glass windows.</p>
                
                <p>Valerius was known for using saffron to achieve brilliant golden colors in his glass work. As a joke for his master's daughter's wedding in 1574, he added saffron to the rice dish being served, creating the golden risotto we know today.</p>
                
                <p>The dish became synonymous with Milanese cuisine and prosperity, as saffron was worth more than gold at the time.</p>''',
                'cultural_context': '''<p>Risotto alla Milanese represents the epitome of Northern Italian cooking philosophy: few ingredients of the highest quality, prepared with meticulous technique. The dish embodies the Milanese values of elegance and sophistication.</p>
                
                <p>Traditionally served alongside osso buco (braised veal shanks), this pairing represents one of the most celebrated combinations in Italian cuisine. The rice absorbs the rich marrow flavors from the meat dish.</p>
                
                <p>In Milan, the preparation of perfect risotto is considered an art form, requiring patience, attention, and the proper technique of constant stirring to release the rice's natural starches.</p>''',
                'ingredients': '''<ul>
                    <li>320g Carnaroli or Arborio rice</li>
                    <li>1.5 liters beef or vegetable broth</li>
                    <li>1 small onion, finely chopped</li>
                    <li>100ml dry white wine</li>
                    <li>50g butter</li>
                    <li>50g grated Parmigiano-Reggiano</li>
                    <li>1 sachet (0.125g) saffron threads</li>
                    <li>2 tablespoons beef bone marrow (optional, traditional)</li>
                    <li>Salt and white pepper to taste</li>
                    <li>Extra virgin olive oil</li>
                </ul>''',
                'instructions': '''<ol>
                    <li><strong>Prepare the saffron:</strong> Soak saffron threads in 2 tablespoons of warm broth. Set aside to infuse.</li>
                    
                    <li><strong>Heat the broth:</strong> Keep the broth simmering in a separate pot throughout the cooking process.</li>
                    
                    <li><strong>Sauté the soffritto:</strong> In a heavy-bottomed pan, heat half the butter with a drizzle of olive oil. Add the finely chopped onion and cook until translucent, about 5 minutes.</li>
                    
                    <li><strong>Toast the rice:</strong> Add the rice and stir for 2-3 minutes until the grains are well-coated and slightly translucent at the edges.</li>
                    
                    <li><strong>Add wine:</strong> Pour in the white wine and stir until completely absorbed.</li>
                    
                    <li><strong>Cook the risotto:</strong> Add hot broth one ladle at a time, stirring constantly. Wait until each addition is almost completely absorbed before adding more. This process takes about 18-20 minutes.</li>
                    
                    <li><strong>Add saffron:</strong> Halfway through cooking, add the saffron with its soaking liquid.</li>
                    
                    <li><strong>Finish with mantecatura:</strong> Remove from heat and vigorously stir in remaining butter and Parmigiano-Reggiano. Season with salt and white pepper.</li>
                    
                    <li><strong>Serve immediately:</strong> The risotto should be creamy and flow like lava when plated. Serve with additional cheese on the side.</li>
                </ol>''',
                'prep_time': 10,
                'cook_time': 25,
                'servings': 4,
                'difficulty': 'medium',
                'image_url': 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'Authentic Butter Chicken (Murgh Makhani)',
                'slug': 'authentic-butter-chicken-murgh-makhani',
                'region': india,
                'category': main_dishes,
                'description': 'Creamy, tomato-based curry with tender chicken, invented in Delhi and beloved worldwide.',
                'history': '''<p>Butter Chicken was invented in the 1950s by Kundan Lal Gujral at his restaurant Moti Mahal in Delhi. Gujral, who had fled from Peshawar during Partition, revolutionized Indian cuisine by introducing the tandoor cooking method to Delhi.</p>
                
                <p>The dish was created almost by accident when Gujral mixed leftover tandoori chicken with tomatoes, butter, and cream to prevent waste. This innovative fusion created one of the most beloved Indian dishes globally.</p>
                
                <p>Gujral's invention not only saved food but also created a new category of Indian cuisine that would influence countless restaurants worldwide, making Indian food more accessible to international palates.</p>''',
                'cultural_context': '''<p>Butter Chicken represents the innovation and adaptability of Indian cuisine, showing how traditional techniques can evolve to create new classics. It bridges the gap between traditional Indian flavors and international tastes.</p>
                
                <p>The dish embodies the spirit of "Jugaad" - the Indian concept of finding innovative solutions with limited resources. What started as a way to use leftovers became a global phenomenon.</p>
                
                <p>In Indian restaurants worldwide, Butter Chicken often serves as an introduction to Indian cuisine for newcomers, its mild heat and creamy texture making it approachable while maintaining authentic flavors.</p>''',
                'ingredients': '''<ul>
                    <li>1kg boneless chicken, cut into pieces</li>
                    <li>200g Greek yogurt</li>
                    <li>1 tablespoon ginger-garlic paste</li>
                    <li>1 teaspoon red chili powder</li>
                    <li>1/2 teaspoon turmeric powder</li>
                    <li>1 teaspoon garam masala</li>
                    <li>Salt to taste</li>
                    <li>2 tablespoons oil</li>
                    <li>4 large tomatoes, pureed</li>
                    <li>1 large onion, finely chopped</li>
                    <li>1 tablespoon ginger-garlic paste</li>
                    <li>1 bay leaf</li>
                    <li>1 teaspoon cumin seeds</li>
                    <li>200ml heavy cream</li>
                    <li>2 tablespoons butter</li>
                    <li>1 teaspoon sugar</li>
                    <li>Fresh cilantro for garnish</li>
                </ul>''',
                'instructions': '''<ol>
                    <li><strong>Marinate the chicken:</strong> Mix chicken with yogurt, ginger-garlic paste, chili powder, turmeric, half the garam masala, and salt. Marinate for at least 2 hours or overnight.</li>
                    
                    <li><strong>Cook the chicken:</strong> Heat oil in a pan and cook marinated chicken until just done. Remove and set aside.</li>
                    
                    <li><strong>Prepare the base:</strong> In the same pan, add cumin seeds and bay leaf. Add chopped onions and cook until golden brown.</li>
                    
                    <li><strong>Add aromatics:</strong> Add ginger-garlic paste and cook for 2 minutes until fragrant.</li>
                    
                    <li><strong>Add tomatoes:</strong> Add tomato puree and cook for 10-15 minutes until the oil separates and the mixture thickens.</li>
                    
                    <li><strong>Blend and strain:</strong> Remove bay leaf and blend the mixture until smooth. Strain for an ultra-smooth texture.</li>
                    
                    <li><strong>Finish the curry:</strong> Return to pan, add cream, butter, sugar, and remaining garam masala. Simmer for 5 minutes.</li>
                    
                    <li><strong>Combine and serve:</strong> Add cooked chicken and simmer for 5 more minutes. Garnish with cilantro and serve with basmati rice and naan.</li>
                </ol>''',
                'prep_time': 30,
                'cook_time': 45,
                'servings': 6,
                'difficulty': 'medium',
                'image_url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'Tom Kha Gai (Thai Coconut Chicken Soup)',
                'slug': 'tom-kha-gai-thai-coconut-chicken-soup',
                'region': thailand,
                'category': soups,
                'description': 'Aromatic Thai soup with coconut milk, galangal, and lime leaves - comfort in a bowl.',
                'history': '''<p>Tom Kha Gai, literally meaning "chicken galangal soup," has been a cornerstone of Thai cuisine for centuries. The dish originated in central Thailand and reflects the country's abundant coconut groves and aromatic herb gardens.</p>
                
                <p>The soup showcases the Thai principle of balancing five fundamental flavors: sweet (coconut milk), sour (lime juice), salty (fish sauce), spicy (chilies), and umami (mushrooms and chicken).</p>
                
                <p>Traditionally prepared as a healing remedy, especially during monsoon season, the soup combines ingredients known for their medicinal properties in traditional Thai medicine.</p>''',
                'cultural_context': '''<p>Tom Kha Gai represents the Thai philosophy of food as medicine. Each ingredient serves both culinary and therapeutic purposes - galangal aids digestion, lemongrass reduces inflammation, and coconut milk provides nourishment.</p>
                
                <p>The soup is often prepared when family members feel unwell, embodying the Thai concept of caring through food. Its gentle flavors make it suitable for all ages, from children to elderly family members.</p>
                
                <p>In Thai culture, sharing soup represents unity and togetherness. Tom Kha Gai is often served family-style, with everyone eating from the same pot, reinforcing communal bonds.</p>''',
                'ingredients': '''<ul>
                    <li>400ml coconut cream</li>
                    <li>200ml chicken stock</li>
                    <li>300g chicken breast, sliced thin</li>
                    <li>4 pieces galangal, sliced</li>
                    <li>3 stalks lemongrass, bruised and cut into 2-inch pieces</li>
                    <li>8-10 kaffir lime leaves, torn</li>
                    <li>200g straw mushrooms, halved</li>
                    <li>3-4 bird's eye chilies, bruised</li>
                    <li>3 tablespoons fish sauce</li>
                    <li>2 tablespoons lime juice</li>
                    <li>1 teaspoon palm sugar</li>
                    <li>Fresh cilantro for garnish</li>
                    <li>Red chili slices for garnish</li>
                </ul>''',
                'instructions': '''<ol>
                    <li><strong>Prepare the aromatic base:</strong> In a pot, heat half the coconut cream over medium heat. Add galangal, lemongrass, and lime leaves. Simmer for 5 minutes to release the aromatics.</li>
                    
                    <li><strong>Add liquid:</strong> Add chicken stock and remaining coconut cream. Bring to a gentle simmer - never boil as this will curdle the coconut milk.</li>
                    
                    <li><strong>Cook the chicken:</strong> Add chicken slices and cook for 3-4 minutes until just cooked through.</li>
                    
                    <li><strong>Add mushrooms:</strong> Add mushrooms and chilies. Simmer for 2-3 minutes until mushrooms are tender.</li>
                    
                    <li><strong>Season the soup:</strong> Add fish sauce, lime juice, and palm sugar. Taste and adjust the balance of salty, sour, and sweet.</li>
                    
                    <li><strong>Final touches:</strong> Remove from heat. The soup should have a perfect balance where no single flavor dominates.</li>
                    
                    <li><strong>Serve immediately:</strong> Ladle into bowls and garnish with fresh cilantro and red chili slices. Serve with jasmine rice.</li>
                </ol>
                
                <p><strong>Note:</strong> The aromatics (galangal, lemongrass, lime leaves) are not typically eaten but provide essential flavor to the broth.</p>''',
                'prep_time': 15,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'Classic French Coq au Vin',
                'slug': 'classic-french-coq-au-vin',
                'region': france,
                'category': main_dishes,
                'description': 'Burgundy wine-braised chicken with mushrooms and pearl onions, a cornerstone of French cuisine.',
                'history': '''<p>Coq au Vin is deeply rooted in French culinary history, with origins possibly dating back to ancient Gaul. Legend attributes the dish to Julius Caesar's conquest of Gaul, where the Gallic chieftain Vercingetorix sent Caesar a rooster as a symbol of Gallic bravery.</p>
                
                <p>Caesar supposedly had the rooster cooked in wine and served it back, symbolizing Rome's dominance. While this story is likely apocryphal, it illustrates the dish's legendary status in French culture.</p>
                
                <p>The dish gained international fame when Julia Child featured it in "Mastering the Art of French Cooking," introducing American cooks to this rustic yet sophisticated preparation.</p>''',
                'cultural_context': '''<p>Coq au Vin embodies the French concept of cuisine bourgeoise - comfort food elevated through technique and quality ingredients. It represents the French ability to transform simple, peasant ingredients into something refined.</p>
                
                <p>The dish showcases the French principle of terroir - using local wine in cooking connects the dish to its specific region, whether Burgundy, Beaujolais, or Champagne, each creating distinct flavor profiles.</p>
                
                <p>Traditionally prepared for Sunday family dinners, Coq au Vin represents French hospitality and the importance of shared meals in maintaining family bonds.</p>''',
                'ingredients': '''<ul>
                    <li>1 whole chicken (1.5-2kg), cut into pieces</li>
                    <li>200g bacon, diced</li>
                    <li>24 pearl onions, peeled</li>
                    <li>250g button mushrooms, quartered</li>
                    <li>3 cloves garlic, minced</li>
                    <li>750ml red wine (Burgundy preferred)</li>
                    <li>2 tablespoons brandy</li>
                    <li>2 bay leaves</li>
                    <li>3 sprigs fresh thyme</li>
                    <li>3 sprigs fresh parsley</li>
                    <li>2 tablespoons flour</li>
                    <li>2 tablespoons butter</li>
                    <li>Salt and freshly ground black pepper</li>
                    <li>Fresh parsley for garnish</li>
                </ul>''',
                'instructions': '''<ol>
                    <li><strong>Prepare the bacon:</strong> In a large, heavy-bottomed pot, cook diced bacon over medium heat until crispy. Remove and set aside, leaving fat in pot.</li>
                    
                    <li><strong>Brown the chicken:</strong> Season chicken pieces with salt and pepper. Brown in bacon fat on all sides until golden. Remove and set aside.</li>
                    
                    <li><strong>Cook vegetables:</strong> Add pearl onions to the pot and brown all over. Add mushrooms and cook until golden. Add garlic and cook for 1 minute.</li>
                    
                    <li><strong>Flambé:</strong> Return chicken to pot. Add brandy and carefully ignite to burn off alcohol. Once flames subside, sprinkle flour over chicken and stir.</li>
                    
                    <li><strong>Add wine and herbs:</strong> Pour in red wine to cover chicken. Add bay leaves, thyme, and parsley tied in a bouquet garni. Bring to a boil.</li>
                    
                    <li><strong>Braise:</strong> Reduce heat to low, cover, and simmer for 45 minutes to 1 hour until chicken is tender and cooked through.</li>
                    
                    <li><strong>Finish and serve:</strong> Remove bouquet garni. Stir in butter and cooked bacon. Adjust seasoning and serve with mashed potatoes or crusty bread.</li>
                </ol>''',
                'prep_time': 30,
                'cook_time': 90,
                'servings': 6,
                'difficulty': 'medium',
                'image_url': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=800&h=600&fit=crop&crop=center'
            }
        ]
        
        for recipe_data in recipes_data:
            if not Recipe.objects.filter(slug=recipe_data['slug']).exists():
                # Remove image_url from recipe_data before creating
                image_url = recipe_data.pop('image_url', None)
                
                recipe = Recipe.objects.create(**recipe_data)
                
                # Add tags
                traditional_tag = Tag.objects.get(name='Traditional')
                recipe.tags.add(traditional_tag)
                
                self.stdout.write(f'Created recipe: {recipe.title}')
    
    def create_articles(self):
        """Create 5 cultural articles"""
        
        articles_data = [
            {
                'title': 'How Migration Shapes Culinary Evolution: The Story of Global Fusion',
                'slug': 'how-migration-shapes-culinary-evolution',
                'article_type': 'blog',
                'excerpt': 'Exploring how human migration patterns have created the fusion cuisines we love today, from Peruvian-Japanese Nikkei to Indian-Chinese dishes.',
                'content': '''<p>Throughout history, human migration has been one of the most powerful forces shaping global cuisine. When people move, they carry their culinary traditions with them, but they also adapt to new ingredients, techniques, and local tastes. This dynamic process has given birth to some of the world's most beloved fusion cuisines.</p>

<h3>The Science of Culinary Adaptation</h3>

<p>When immigrants settle in new countries, they face immediate challenges: familiar ingredients may be unavailable or expensive, and local tastes might differ dramatically from home. This necessity drives innovation. Chinese immigrants to India created dishes like Hakka noodles and Manchurian chicken - foods that exist nowhere in China but have become integral to Indian-Chinese cuisine.</p>

<p>Similarly, Japanese immigrants to Peru in the early 20th century couldn't find traditional ingredients like miso or short-grain rice. They adapted by using local Peruvian ingredients, creating Nikkei cuisine - a fusion that combines Japanese techniques with Peruvian flavors, giving us dishes like tiradito and nikkei sushi.</p>

<h3>Economic and Social Factors</h3>

<p>Migration-driven cuisine evolution isn't just about ingredient availability - it's deeply influenced by economic and social factors. Italian immigrants to America created Italian-American cuisine by adapting their traditional recipes to local tastes and available ingredients. Dishes like chicken parmigiana and spaghetti with meatballs were created to appeal to American palates while maintaining Italian cooking principles.</p>

<blockquote>
"Food is the great connector. It transcends language barriers and cultural differences, becoming a bridge between the old world and the new." - Chef Marcus Samuelsson
</blockquote>

<h3>Modern Migration and Digital Influence</h3>

<p>Today's migration patterns are creating even more complex fusion cuisines. Korean immigrants have brought kimchi to Mexican tacos, creating Korean-Mexican fusion. Vietnamese immigrants have adapted their pho to local tastes in different countries, resulting in variations you'll find nowhere in Vietnam.</p>

<p>Social media and food blogs accelerate this process, allowing fusion recipes to spread globally within months rather than generations. A dish created by a Vietnamese-American chef in Los Angeles can influence Vietnamese restaurants in Australia within weeks.</p>

<h3>Preserving Authenticity While Embracing Change</h3>

<p>The challenge for immigrant communities is maintaining their culinary identity while adapting to new environments. Many families develop "home versions" and "restaurant versions" of traditional dishes - keeping authentic recipes alive within families while serving adapted versions to broader audiences.</p>

<p>This dual approach has proven essential for cultural preservation. The most successful fusion cuisines maintain core principles of their origin culture while embracing local innovations.</p>

<h3>Looking Forward</h3>

<p>As climate change and economic opportunities continue to drive global migration, we can expect even more culinary innovation. African cuisines are beginning to influence global food scenes as African diaspora communities grow worldwide. Plant-based diets are pushing traditional meat-based cuisines to innovate with vegetables and alternative proteins.</p>

<p>The story of migration and food is ultimately a story of human resilience and creativity. Every fusion dish tells a story of adaptation, survival, and the universal human desire to maintain connections to home while building new communities.</p>''',
                'image_url': 'https://images.unsplash.com/photo-1556909114-4b48d4a6e75b?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'Bread Traditions Around the World: Unity in Diversity',
                'slug': 'bread-traditions-around-the-world',
                'article_type': 'culture',
                'excerpt': 'From naan to sourdough, discover how different cultures have developed unique bread-making traditions using similar basic ingredients.',
                'content': '''<p>Bread, in its countless forms, represents one of humanity's most fundamental foods. Despite vast cultural differences, nearly every civilization has developed some form of bread, using locally available grains and adapting techniques to their environment and needs.</p>

<h3>The Universal Language of Grain</h3>

<p>At its core, bread requires only grain, water, and time. Yet from these simple ingredients, human ingenuity has created thousands of variations. In Ethiopia, injera is made from teff flour, creating a spongy, slightly sour flatbread that serves both as food and plate. In Mexico, corn tortillas represent a 9,000-year-old tradition that predates wheat cultivation in the Americas.</p>

<p>The choice of grain often reflects geographical limitations and cultural preferences. Barley was the grain of choice in ancient Egypt and Greece, while rice-based breads developed across Asia. Rye bread became essential in Northern European countries where wheat struggled to grow in harsh climates.</p>

<h3>Fermentation: Nature's Gift to Bread</h3>

<p>The discovery of fermentation revolutionized bread-making, though it likely happened by accident. Wild yeasts naturally occurring in the environment would begin fermenting grain mixtures left exposed to air. Different regions developed different fermentation cultures based on their local microbial environments.</p>

<p>San Francisco sourdough gets its distinctive tang from Lactobacillus sanfranciscensis, a bacteria strain unique to that region's fog-cooled environment. Similarly, German rye breads develop their characteristic flavors from centuries-old starter cultures passed down through generations of bakers.</p>

<blockquote>
"Bread is the warmest, kindest of words. Write it always with a capital letter, like your own name." - Russian Proverb
</blockquote>

<h3>Bread as Social Connector</h3>

<p>Beyond nutrition, bread plays crucial social and spiritual roles across cultures. In many Middle Eastern and Mediterranean cultures, breaking bread together creates bonds of hospitality and trust. The Arabic phrase "we have shared bread and salt" signifies an unbreakable bond between people.</p>

<p>Jewish challah bread marks the Sabbath with its braided shape symbolizing unity and continuity. Hindu cultures consider bread-making a sacred act, with specific prayers offered during kneading and baking. Indigenous American corn breads often incorporate ceremonial elements, connecting the community to ancestral traditions.</p>

<h3>Techniques Shaped by Environment</h3>

<p>Climate and available fuel sources heavily influenced bread-making techniques. In the Mediterranean, wood-fired communal ovens became centers of village life, with families bringing their bread to be baked together. Desert cultures developed flatbreads that could be cooked quickly on hot stones or metal surfaces.</p>

<p>In Northern climates, dense, long-lasting breads like German pumpernickel or Scandinavian crispbreads were developed to withstand harsh winters. These breads could be stored for months, providing sustenance when fresh baking wasn't possible.</p>

<h3>Modern Globalization and Tradition</h3>

<p>Today's global food culture allows us to experience bread traditions from around the world. Japanese shokupan's pillowy texture influences American sandwich breads. Indian naan has become as common as pizza in many Western cities. French baguette techniques are taught in cooking schools worldwide.</p>

<p>Yet this globalization also threatens traditional methods. Industrial bread production prioritizes speed and uniformity over flavor and nutrition. Many traditional grains and techniques risk being lost as commercial varieties dominate markets.</p>

<h3>The Artisan Revival</h3>

<p>Fortunately, a growing movement of artisan bakers worldwide is reviving traditional techniques. Ancient grains like einkorn, emmer, and spelt are being reintroduced. Traditional fermentation methods are being taught to new generations of bakers committed to preserving these cultural treasures.</p>

<p>Home baking surged during the COVID-19 pandemic, with people rediscovering the meditative process of kneading dough and the satisfaction of creating bread from basic ingredients. This renewed interest in bread-making represents more than a hobby - it's a reconnection with fundamental human traditions.</p>

<p>As we look to the future, bread continues to evolve. Gluten-free breads serve those with dietary restrictions. Plant-based enrichments replace traditional dairy and eggs. Climate-adapted grains are being developed for changing growing conditions.</p>

<p>Yet regardless of these innovations, bread remains what it has always been: a testament to human creativity, community, and our ability to transform simple ingredients into something greater than the sum of their parts.</p>''',
                'image_url': 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'Food as Diplomacy: Meals That Changed History',
                'slug': 'food-as-diplomacy-meals-that-changed-history',
                'article_type': 'blog',
                'excerpt': 'From Nixon\'s visit to China to state dinners that prevented wars, explore how carefully planned meals have shaped international relations.',
                'content': '''<p>Throughout history, some of the world's most significant diplomatic breakthroughs have happened not in formal meeting rooms, but around dinner tables. The careful selection of menus, the symbolism of shared meals, and the informal atmosphere of dining have often achieved what formal negotiations could not.</p>

<h3>The Great Banquet Diplomacy</h3>

<p>One of the most famous examples of culinary diplomacy occurred during President Nixon's historic 1972 visit to China. Premier Zhou Enlai's choice to serve both Chinese and Western dishes at the welcoming banquet was deeply symbolic. The menu included Peking duck alongside Western-style soup, representing the bridge between two vastly different cultures.</p>

<p>The banquet's success lay not just in the food, but in the act of sharing it. Nixon's willingness to use chopsticks and try unfamiliar dishes showed respect for Chinese culture, while Zhou's inclusion of familiar Western elements demonstrated Chinese hospitality and understanding.</p>

<h3>The Camp David Accords and Middle Eastern Cuisine</h3>

<p>President Jimmy Carter's choice to include Middle Eastern dishes during the 1978 Camp David negotiations between Egyptian President Anwar Sadat and Israeli Prime Minister Menachem Begin was strategically brilliant. By serving foods familiar to both leaders, Carter created an atmosphere of comfort and shared cultural heritage.</p>

<p>The informal meals, often eaten together without protocol officers present, allowed the leaders to connect on a human level. Sadat and Begin discovered shared memories of similar dishes from their youth, creating unexpected moments of warmth during tense negotiations.</p>

<blockquote>
"The way to a man's heart is through his stomach, but the way to peace might be through his palate." - Anonymous diplomatic observer
</blockquote>

<h3>State Dinners as Cultural Bridges</h3>

<p>Modern state dinners have evolved into carefully choreographed cultural exchanges. When French President Emmanuel Macron visited the White House in 2018, the menu deliberately included both American and French elements - highlighting the historical alliance while respecting both culinary traditions.</p>

<p>The choice of American wine for the dinner was particularly symbolic, acknowledging French influence on American winemaking while showcasing American agricultural achievements. Such details, often overlooked by casual observers, send powerful messages to diplomatic communities.</p>

<h3>Breaking Bread to Break Barriers</h3>

<p>The Islamic tradition of sharing salt creates a bond of protection and hospitality that has influenced Middle Eastern diplomacy for centuries. During the Ottoman Empire, elaborate feasts were used to display power while also creating obligations of reciprocity among guests.</p>

<p>Similar traditions exist worldwide: in many African cultures, refusing offered food is considered an insult that can end negotiations before they begin. Understanding these cultural nuances has often meant the difference between diplomatic success and failure.</p>

<h3>The United Nations and Culinary Diplomacy</h3>

<p>The United Nations regularly uses food as a diplomatic tool. National delegations often host cultural food events to showcase their countries and build informal relationships with other diplomats. These casual interactions, often over shared meals, frequently lead to formal cooperation agreements.</p>

<p>The UN's "Friendship Bench" program pairs diplomats from different countries for informal lunches, explicitly using food as a mechanism for building personal relationships that translate into political understanding.</p>

<h3>Modern Challenges and Opportunities</h3>

<p>Today's diplomatic dining faces new challenges: dietary restrictions, religious considerations, and environmental concerns all factor into menu planning. Vegan state dinners are becoming more common, reflecting growing environmental awareness and inclusivity concerns.</p>

<p>The COVID-19 pandemic forced diplomacy online, highlighting how much we rely on shared meals for relationship building. Virtual wine tastings and cooking demonstrations attempted to replicate the bonding experience of eating together, with mixed success.</p>

<h3>The Psychology of Shared Meals</h3>

<p>Research confirms what diplomats have long known: people who eat together are more likely to trust each other and find common ground. The act of sharing food triggers evolutionary responses that promote cooperation and reduce aggression.</p>

<p>Neuroscientists have found that eating activates the brain's reward centers, creating positive associations with present company. This biological response explains why "breaking bread" has become synonymous with peace-making across cultures.</p>

<h3>Looking to the Future</h3>

<p>As climate change and food security become major global challenges, culinary diplomacy may play an even larger role in international relations. Shared meals focusing on sustainable ingredients and traditional preservation techniques could become platforms for discussing environmental cooperation.</p>

<p>The growing global food movement also creates opportunities for citizen diplomacy - cultural food exchanges, international cooking classes, and food-focused sister city programs all contribute to international understanding at grassroots levels.</p>

<p>Ultimately, food diplomacy succeeds because it appeals to our most basic human needs: sustenance, community, and recognition. In a world often divided by politics and ideology, the universal need to eat provides common ground where understanding can begin.</p>''',
                'image_url': 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'The Art of Fermentation: Ancient Wisdom for Modern Health',
                'slug': 'the-art-of-fermentation-ancient-wisdom',
                'article_type': 'culture',
                'excerpt': 'Discover how traditional fermentation techniques from cultures worldwide are revolutionizing our understanding of gut health and sustainable food production.',
                'content': '''<p>Long before humans understood bacteria and microorganisms, they discovered that controlled decomposition could transform food into something more nutritious, flavorful, and longer-lasting. Today, as we face challenges of health, sustainability, and food security, these ancient fermentation traditions offer profound wisdom.</p>

<h3>The Universal Discovery</h3>

<p>Fermentation appears in virtually every culture because it solves fundamental human needs: preservation without refrigeration, enhanced nutrition, and improved digestibility. Korean kimchi, German sauerkraut, Indian dosas, and African injera all represent independent discoveries of similar principles by different civilizations.</p>

<p>What's remarkable is how consistently these cultures developed not just functional fermented foods, but traditions that recognized their health benefits. Traditional Chinese medicine has long prescribed fermented foods for digestive health, while Indian Ayurveda considers fermented foods essential for maintaining proper gut bacteria.</p>

<h3>The Science Behind Ancient Wisdom</h3>

<p>Modern research has validated what traditional cultures knew intuitively. Fermented foods contain beneficial bacteria (probiotics) that support digestive health and immune function. The fermentation process also creates new nutrients: vitamin K2 in fermented dairy, vitamin B12 in some fermented vegetables, and enhanced bioavailability of minerals.</p>

<p>Lacto-fermentation, used in making traditional pickles and sauerkraut, produces lactobacillus bacteria that can survive stomach acid and colonize the intestine. These bacteria produce short-chain fatty acids that reduce inflammation and may protect against various diseases.</p>

<blockquote>
"In fermentation, we see the beautiful partnership between humans and microorganisms - a collaboration that has sustained us for millennia." - Sandor Katz, fermentation expert
</blockquote>

<h3>Cultural Preservation Through Microorganisms</h3>

<p>Each region's fermented foods contain unique microbial communities adapted to local environments. Tibetan yak cheese contains bacteria that thrive at high altitudes. Japanese miso develops differently based on regional temperature and humidity patterns. These microbial terroirs are as distinctive as wine regions.</p>

<p>Sadly, industrialization threatens these microbial ecosystems. Commercial pasteurization kills beneficial bacteria, while standardized starter cultures replace diverse local strains. When traditional fermentation practices disappear, we lose not just recipes but entire ecosystems of beneficial microorganisms.</p>

<h3>Fermentation and Sustainability</h3>

<p>Traditional fermentation offers solutions to modern sustainability challenges. Fermented foods require no refrigeration during production and have extended shelf lives, reducing energy consumption and food waste. Plant-based fermentation can create protein-rich foods from locally available ingredients.</p>

<p>Indonesian tempeh transforms soybeans into a complete protein through fermentation, providing meat-like nutrition with a fraction of the environmental impact. African fermented legume pastes serve similar functions, creating nutrient-dense foods from drought-resistant crops.</p>

<h3>The Ritual and Community Aspects</h3>

<p>In many cultures, fermentation involves community participation and ceremonial elements. Japanese families gather annually to make miso, with recipes and techniques passed down through generations. The process becomes a way of maintaining cultural identity and family bonds.</p>

<p>Ethiopian women often ferment injera batter communally, sharing starter cultures and techniques. This sharing ensures genetic diversity in fermentation cultures while strengthening social connections. The timing of fermentation - often several days - requires patience and planning that connects people to natural rhythms.</p>

<h3>Modern Applications and Innovations</h3>

<p>Contemporary chefs and food scientists are rediscovering fermentation's potential. Restaurants like Copenhagen's Noma have elevated fermentation to haute cuisine, while food entrepreneurs are creating new products based on traditional techniques.</p>

<p>Plant-based meat alternatives increasingly use fermentation to develop complex flavors and textures. Cellular agriculture companies are exploring fermentation for producing animal proteins without animals. These innovations build on ancient knowledge while addressing modern dietary needs.</p>

<h3>The Home Fermentation Revival</h3>

<p>Interest in home fermentation has exploded as people seek healthier, more sustainable food options. Online communities share starter cultures and techniques, creating global networks of fermentation enthusiasts. This democratization of knowledge helps preserve traditional methods while encouraging innovation.</p>

<p>The COVID-19 pandemic accelerated this trend as people had more time at home and greater interest in immune-supporting foods. Kombucha, kimchi, and sourdough bread became pandemic staples for many households.</p>

<h3>Challenges and Opportunities</h3>

<p>Despite growing interest, fermentation faces challenges in our sanitized modern world. Fear of "bad" bacteria leads many to avoid fermented foods or rely only on pasteurized versions. Food safety regulations sometimes favor industrial processes over traditional methods.</p>

<p>Education is crucial for overcoming these barriers. Understanding that humans evolved alongside beneficial microorganisms helps people appreciate fermentation's safety when done properly. Traditional fermentation methods have sustained communities for thousands of years without modern sterile environments.</p>

<h3>The Future of Fermentation</h3>

<p>As we face climate change and growing global populations, fermentation offers scalable solutions. Fermented foods can be produced locally using available ingredients, reducing transportation costs and carbon emissions. They provide nutrition security by extending food shelf life and enhancing nutrient availability.</p>

<p>The convergence of traditional knowledge and modern science promises exciting developments. Researchers are identifying specific probiotic strains for targeted health benefits while food artisans explore new flavor possibilities through controlled fermentation.</p>

<p>Ultimately, fermentation represents a profound partnership between humans and microorganisms - one that has sustained us throughout history and offers hope for a healthier, more sustainable future. By honoring traditional wisdom while embracing scientific understanding, we can unlock fermentation's full potential for modern challenges.</p>''',
                'image_url': 'https://images.unsplash.com/photo-1556909114-79a35b8d7c08?w=800&h=600&fit=crop&crop=center'
            },
            {
                'title': 'Street Food Chronicles: The Soul of City Cuisine',
                'slug': 'street-food-chronicles-soul-of-city-cuisine',
                'article_type': 'story',
                'author_name': 'Maria Elena Vasquez',
                'author_bio': 'Food anthropologist and street food researcher who has documented culinary traditions across six continents. Author of "Sidewalk Sustenance: A Global Journey Through Street Food Culture."',
                'excerpt': 'A journey through the world\'s street food capitals reveals how these humble vendors preserve culinary traditions while creating new fusion flavors.',
                'content': '''<p>At 5 AM in Bangkok, the smell of charcoal and frying garlic fills the air as street vendors begin their daily ritual. By evening, Mexico City's food trucks will serve thousands of tacos. In Mumbai, dabbawallas will complete their legendary lunch delivery system. Street food isn't just about quick meals - it's the heartbeat of urban culture.</p>

<h3>The Democracy of Deliciousness</h3>

<p>Street food represents the ultimate democratic cuisine. A construction worker and a bank executive might stand side by side at the same cart, united by their appreciation for perfectly seasoned food served at accessible prices. This equality of access creates a unique social dynamic found nowhere else in urban dining.</p>

<p>I've observed this phenomenon across continents: In Istanbul, the döner kebab vendor serves everyone from university students to business executives. In Bangkok, office workers in expensive suits sit on plastic stools eating som tam from the same vendor as motorcycle taxi drivers. Street food erases economic and social boundaries in ways few other cultural experiences can match.</p>

<h3>Guardians of Culinary Heritage</h3>

<p>Street vendors often serve as unexpected guardians of traditional recipes. While restaurants may modify dishes for tourist palates or upscale presentations, street food vendors typically maintain authentic preparations passed down through families or learned through informal apprenticeships.</p>

<p>In Oaxaca, Mexico, I met Doña Carmen, whose mole recipe came from her grandmother. She's been making the same twenty-ingredient sauce for thirty years, serving it from a small cart near the market. Her mole represents a direct link to pre-Hispanic cooking traditions that fancy restaurants often oversimplify.</p>

<blockquote>
"Street food is honest food. We can't hide behind fancy plating or expensive ingredients. The food must speak for itself." - Raj Kumar, Mumbai street vendor
</blockquote>

<h3>Innovation Born from Necessity</h3>

<p>Limited equipment and space force street vendors to develop incredible efficiency and creativity. Korean corn dogs filled with cheese and coated in ramen noodles emerged from vendors seeking ways to differentiate their offerings. Taiwanese beef noodle soup evolved from Chinese refugees adapting traditional recipes to local ingredients and quick service needs.</p>

<p>In Lima, Peru, I watched vendors create fusion dishes that reflect the city's diverse population. Chinese-Peruvian chifa influences blend with traditional Andean ingredients in ways that formal restaurants rarely attempt. These innovations often start on street corners before being adopted by upscale establishments.</p>

<h3>The Economics of Street Food</h3>

<p>Street food provides economic opportunities for people with limited capital but abundant culinary skills. A cart or small stall requires far less investment than a restaurant, making entrepreneurship accessible to immigrants, women, and economically disadvantaged populations.</p>

<p>In many developing cities, street food vendors support entire extended families through their businesses. They employ relatives, source ingredients from local farmers, and contribute significantly to urban economies. In Bangkok alone, street food generates billions of dollars annually while employing hundreds of thousands of people.</p>

<h3>Cultural Fusion in Real Time</h3>

<p>Street food serves as a laboratory for cultural fusion. When immigrants establish food stalls, they adapt their traditional recipes to local tastes and available ingredients. This creates new dishes that bridge cultures in ways formal restaurants, bound by tradition or chef egos, might not attempt.</p>

<p>Los Angeles food trucks exemplify this phenomenon. Korean-Mexican fusion emerged from Korean immigrants serving their food in predominantly Latino neighborhoods. The resulting kimchi quesadillas and bulgogi tacos represent genuine cultural exchange, not marketing-driven fusion.</p>

<h3>The Sensory Theater of Street Food</h3>

<p>Street food engages all senses in ways restaurant dining cannot match. The sizzle of onions hitting hot oil, the rhythmic chopping of vegetables, the theatrical flames from wok cooking - these performances are integral to the experience. Diners witness their food's creation, creating trust and anticipation.</p>

<p>In Mumbai, watching a pav bhaji vendor's choreographed movements - simultaneously mashing vegetables, toasting bread, and serving customers - is performance art. The vendor's skill becomes part of the meal's value, entertainment included with every order.</p>

<h3>Challenges Facing Street Food Culture</h3>

<p>Modernization threatens traditional street food in many cities. Gentrification displaces long-established vendors, while health regulations often favor formal restaurants over street operations. Food courts and malls attempt to recreate street food atmospheres but lose the authentic cultural context.</p>

<p>Climate change also poses challenges. Extreme weather events disrupt vendor operations, while changing precipitation patterns affect ingredient availability. Vendors adapt with covered stalls and modified menus, but these changes alter traditional preparation methods.</p>

<h3>Technology and Tradition</h3>

<p>Modern technology is transforming street food while preserving its essential character. Mobile payment systems make transactions easier, while social media helps vendors build customer bases and receive feedback. GPS tracking allows food trucks to notify customers of their locations in real time.</p>

<p>However, successful vendors balance technological adoption with traditional practices. The most popular food trucks still rely on family recipes and personal relationships with customers. Technology enhances accessibility but doesn't replace the human connections that make street food special.</p>

<h3>The Future of Street Food</h3>

<p>As urbanization accelerates globally, street food culture will continue evolving. Rising food costs and environmental concerns may increase demand for affordable, locally-sourced meals that street vendors traditionally provide. Plant-based street food options are emerging to meet changing dietary preferences.</p>

<p>Food halls and night markets represent attempts to preserve street food culture while addressing modern urban challenges. These spaces maintain the diversity and accessibility of traditional street food while providing vendors with more secure locations and customers with comfortable environments.</p>

<h3>Why Street Food Matters</h3>

<p>Street food matters because it represents authentic urban culture in its purest form. It feeds cities, preserves traditions, enables entrepreneurship, and creates community. In an increasingly homogenized world, street food vendors maintain local flavors and cultural distinctiveness.</p>

<p>Every street food experience tells a story - of immigration, adaptation, tradition, and innovation. These humble vendors serve more than food; they serve as cultural ambassadors, economic engines, and guardians of culinary heritage. Their continued success represents the resilience of human creativity and the universal power of sharing good food.</p>''',
                'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=600&fit=crop&crop=center'
            }
        ]
        
        for article_data in articles_data:
            if not Article.objects.filter(slug=article_data['slug']).exists():
                # Remove image_url from article_data before creating
                image_url = article_data.pop('image_url', None)
                
                article = Article.objects.create(**article_data)
                
                self.stdout.write(f'Created article: {article.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample content!'))
