import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from newsapp.models import Category, Source, News, NewsCategory, Comment, Bookmark, UserPreference

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database...')
        
        # Create categories
        categories = [
            'Politics', 'Technology', 'Business', 'Science', 'Health', 
            'Entertainment', 'Sports', 'World', 'Environment', 'Education'
        ]
        
        category_objects = []
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            category_objects.append(category)
            if created:
                self.stdout.write(f'Created category: {category_name}')
        
        # Create sources
        sources = [
            {
                'name': 'TechCrunch',
                'website_url': 'https://techcrunch.com',
                'country': 'United States'
            },
            {
                'name': 'BBC News',
                'website_url': 'https://bbc.com/news',
                'country': 'United Kingdom'
            },
            {
                'name': 'Der Spiegel',
                'website_url': 'https://spiegel.de',
                'country': 'Germany'
            },
            {
                'name': 'Al Jazeera',
                'website_url': 'https://aljazeera.com',
                'country': 'Qatar'
            },
            {
                'name': 'The Guardian',
                'website_url': 'https://theguardian.com',
                'country': 'United Kingdom'
            },
        ]
        
        source_objects = []
        for source_data in sources:
            source, created = Source.objects.get_or_create(
                name=source_data['name'],
                defaults={
                    'website_url': source_data['website_url'],
                    'country': source_data['country']
                }
            )
            source_objects.append(source)
            if created:
                self.stdout.write(f'Created source: {source.name}')
        
        # Create sample news articles
        news_articles = [
            {
                'title': 'New AI Algorithm Achieves Breakthrough in Protein Folding',
                'content': """Scientists have developed a new artificial intelligence algorithm that can predict 
                protein structures with unprecedented accuracy. This breakthrough could accelerate drug discovery 
                and our understanding of diseases. The research team, led by Dr. Jane Smith, published their findings 
                in the journal Nature yesterday. "This is a significant step forward in the field of computational biology," 
                said Dr. Smith.""",
                'author': 'Michael Johnson',
                'image_url': 'https://example.com/images/ai_protein.jpg',
                'source': 'TechCrunch',
                'categories': ['Technology', 'Science', 'Health']
            },
            {
                'title': 'Global Climate Summit Reaches Historic Agreement',
                'content': """World leaders have reached a landmark agreement at the Global Climate Summit to reduce 
                carbon emissions by 50% by 2030. The agreement, signed by 195 countries, represents the most ambitious 
                climate action plan to date. "This is a historic day for our planet," said UN Secretary-General in his 
                closing speech. Experts say the implementation of the agreement will require significant changes in 
                energy production and consumption worldwide.""",
                'author': 'Sarah Williams',
                'image_url': 'https://example.com/images/climate_summit.jpg',
                'source': 'BBC News',
                'categories': ['Environment', 'World', 'Politics']
            },
            {
                'title': 'Major Tech Companies Announce Joint Quantum Computing Initiative',
                'content': """Five of the world's largest technology companies have announced a collaborative initiative 
                to advance quantum computing research. The project aims to develop a practical quantum computer within 
                the next decade. "By pooling our resources and expertise, we can accelerate progress in this critical field," 
                said the CEO of one participating company. The initiative will include shared research facilities and 
                an open-source approach to basic algorithms.""",
                'author': 'David Chen',
                'image_url': 'https://example.com/images/quantum_computing.jpg',
                'source': 'TechCrunch',
                'categories': ['Technology', 'Business', 'Science']
            },
            {
                'title': 'New Educational Policy Aims to Bridge Digital Divide',
                'content': """The government has unveiled a new educational policy focused on addressing the digital 
                divide in schools. The initiative will provide tablets and internet access to students in underserved 
                communities. "Every child deserves equal access to digital learning tools," said the Education Minister. 
                The program will be implemented in phases over the next three years, with the first phase targeting 
                rural schools.""",
                'author': 'Amanda Rodriguez',
                'image_url': 'https://example.com/images/education_digital.jpg',
                'source': 'The Guardian',
                'categories': ['Education', 'Technology', 'Politics']
            },
            {
                'title': 'Breakthrough in Renewable Energy Storage Announced',
                'content': """Researchers have developed a new type of battery that could solve one of the biggest 
                challenges in renewable energy: efficient storage. The new technology can store energy for up to 
                a week with minimal loss and is made from abundant, non-toxic materials. "This could be the missing 
                piece in the renewable energy puzzle," said Professor Mark Thompson, lead researcher. Industry experts 
                say the technology could be commercially viable within five years.""",
                'author': 'Elena Schwarz',
                'image_url': 'https://example.com/images/energy_storage.jpg',
                'source': 'Der Spiegel',
                'categories': ['Science', 'Technology', 'Environment']
            },
            {
                'title': 'International Space Station Begins New Research Mission',
                'content': """The International Space Station has begun a new series of experiments that could have 
                far-reaching implications for future space exploration. The research focuses on the effects of 
                microgravity on advanced materials manufacturing. "What we learn here could revolutionize how we 
                produce certain materials both in space and on Earth," said astronaut John Miller. The experiments 
                are scheduled to continue for the next six months.""",
                'author': 'James Wilson',
                'image_url': 'https://example.com/images/iss_research.jpg',
                'source': 'Al Jazeera',
                'categories': ['Science', 'Technology']
            },
            {
                'title': 'Global Economic Forum Predicts Strong Recovery',
                'content': """The Global Economic Forum has released its annual forecast, predicting a stronger than 
                expected economic recovery in the coming year. The report cites increased consumer spending and 
                infrastructure investments as key factors. "While challenges remain, the overall trajectory is positive," 
                said the Forum's chief economist. The forecast particularly highlights growth opportunities in the 
                green energy sector and digital services.""",
                'author': 'Robert Garcia',
                'image_url': 'https://example.com/images/economic_recovery.jpg',
                'source': 'BBC News',
                'categories': ['Business', 'World', 'Politics']
            },
            {
                'title': 'New Treatment Shows Promise for Alzheimer\'s Disease',
                'content': """Clinical trials for a new Alzheimer's treatment have shown promising results, according 
                to research published today. The drug, which targets protein buildup in the brain, slowed cognitive 
                decline by 32% in early-stage patients. "These results give us hope that we're finally making progress 
                against this devastating disease," said Dr. Laura Martinez, who led the study. Researchers caution that 
                larger trials are still needed before the treatment can be widely approved.""",
                'author': 'Thomas Brown',
                'image_url': 'https://example.com/images/alzheimers_treatment.jpg',
                'source': 'The Guardian',
                'categories': ['Health', 'Science']
            },
            {
                'title': 'Major Sports League Announces Expansion Teams',
                'content': """The professional sports landscape is set to change with the announcement of two new 
                expansion teams joining the major league next season. The new franchises will be based in Nashville 
                and San Diego, bringing the total number of teams to 32. "This expansion represents the growing 
                popularity of our sport across the country," said the league commissioner. Each new team will 
                participate in an expansion draft to build their initial rosters.""",
                'author': 'Jessica Taylor',
                'image_url': 'https://example.com/images/sports_expansion.jpg',
                'source': 'Al Jazeera',
                'categories': ['Sports', 'Business']
            },
            {
                'title': 'Award-Winning Film Director Announces New Project',
                'content': """Acclaimed film director Alexandra Reyes has announced her next project, an adaptation 
                of the bestselling novel "Echoes of Tomorrow." The film will begin production next month with an 
                all-star cast. "I've been wanting to bring this story to the screen for years," said Reyes in a 
                press conference. The project has already generated significant buzz in the entertainment industry, 
                with many predicting it will be a major awards contender.""",
                'author': 'Kevin Morris',
                'image_url': 'https://example.com/images/film_director.jpg',
                'source': 'Der Spiegel',
                'categories': ['Entertainment']
            }
        ]
        
        # Create a test user if it doesn't exist
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_active': True,
            }
        )
        
        if created:
            test_user.set_password('testpassword')
            test_user.save()
            self.stdout.write(f'Created test user: {test_user.username}')
            
            # Create user preferences
            UserPreference.objects.create(user=test_user)
            self.stdout.write(f'Created preferences for user: {test_user.username}')
        
        # Create news articles and associate with categories
        now = timezone.now()
        
        for idx, article_data in enumerate(news_articles):
            # Find the source
            source = next((s for s in source_objects if s.name == article_data['source']), source_objects[0])
            
            # Create the news article
            published_date = now - timedelta(days=idx, hours=random.randint(0, 23), minutes=random.randint(0, 59))
            
            news, created = News.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'content': article_data['content'],
                    'author': article_data['author'],
                    'image_url': article_data['image_url'],
                    'published_at': published_date,
                    'source': source,
                    'is_read': False,
                    'url': f"{source.website_url}/article{idx}"
                }
            )
            
            if created:
                self.stdout.write(f'Created news article: {news.title}')
                
                # Associate with categories
                for category_name in article_data['categories']:
                    category = next((c for c in category_objects if c.name == category_name), None)
                    if category:
                        NewsCategory.objects.get_or_create(news=news, category=category)
                        self.stdout.write(f'  - Added to category: {category.name}')
                
                # Create a comment
                if random.random() > 0.5:  # 50% chance of having a comment
                    comment = Comment.objects.create(
                        user=test_user,
                        news=news,
                        content=f"This is a sample comment on the article about {news.title.lower()}.",
                        created_at=published_date + timedelta(hours=random.randint(1, 5))
                    )
                    self.stdout.write(f'  - Added comment by {test_user.username}')
                
                # Create a bookmark
                if random.random() > 0.7:  # 30% chance of being bookmarked
                    bookmark = Bookmark.objects.create(
                        user=test_user,
                        news=news,
                        saved_at=published_date + timedelta(hours=random.randint(1, 10))
                    )
                    self.stdout.write(f'  - Bookmarked by {test_user.username}')
        
        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))
        self.stdout.write(self.style.SUCCESS('Login with username: testuser and password: testpassword')) 