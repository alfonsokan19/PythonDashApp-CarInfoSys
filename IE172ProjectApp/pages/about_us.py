import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



layout = html.Div(children=[
    html.H1(children='About Us'),
    html.Hr(),
    html.Div(children=[
        html.P(
            "Welcome to Winston's Automobiles!"
        ),

        html.H2("Who We Are"),
        html.Hr(),
        html.P(
            "Winston's Automobiles is a dedicated and family-owned business specializing in the buying and selling of high-quality and affordable"
            "second-hand cars. With a rich legacy in the automotive industry and a deep commitment to excellence, we take pride in offering a curated" 
            "selection of pre-owned vehicles that meet the highest standards of quality and reliability."
        ),
        dcc.Markdown(
                    '''
                    **Winstons Automobiles** is a family owned business that started in 1999, and they buy and sell second-hand cars.
                    Their business started with selling a singular car and eventually grew to a medium-sized operation that is simultaneously selling around 10 or more cars all at once.
                    Their business has two primary goals:
                    (1) to buy second-hand cars that are well maintained, having its original papers complete with no outstanding debts or warrants;
                    (2) and to sell high-quality second-hand cars such that the buyers will not have any immediate problems or concerns regarding the vehicle. Achieving these goals would not only allow them to have a steady stream of income but would also allow them to build a respectable name and network in the field.
                    '''
                ),

        html.H2("Our Mission"),
        html.Hr(),
        html.P(
            "At Winston's Automobiles, our mission is to redefine the pre-owned car buying experience by providing a curated selection of high-quality and affordable second-hand cars."
            "We are dedicated to fostering trust, transparency, and satisfaction among our customers, ensuring that each family finds the perfect vehicle that not only meets their needs but also exceeds their expectations. Through our commitment to excellence, we aim to become the go-to destination for families"
            "seeking reliable and budget-friendly pre-owned cars, creating lasting relationships built on integrity and exceptional service."
        ),

        html.H2("What Sets Us Apart"),
        html.Hr(),
        html.H3("Expertise"),
        html.P(
            "Backed by generations of automotive expertise, we pride ourselves on our in-depth knowledge of high-quality second-hand cars."
            "Our team of seasoned professionals possesses a deep understanding of the market, enabling us to handpick and thoroughly inspect each vehicle"
            "in our inventory. This expertise ensures that every car meets our stringent standards for quality, reliability, and performance. When you"
            "choose Winston's Automobiles, you benefit from the assurance that comes with decades of industry knowledge and a genuine passion for cars."
        ),

        html.H3("Innovation"),
        html.P(
            "At the heart of our business is a commitment to innovation. We leverage cutting-edge technologies and modern business practices to streamline the"
            "car-buying process. From advanced inspection methods to digital platforms that enhance transparency and convenience, we continuously seek innovative"
            "solutions. Our forward-thinking approach ensures that our customers experience a seamless and efficient journey, from browsing our inventory to driving"
            "off in their chosen vehicle. At Winston's Automobiles, we embrace innovation as a means to enhance the overall customer experience and redefine."
            "the standards in the pre-owned car industry "
        ),

        html.H3("User-Centric Design"),
        html.P(
            "Our business revolves around you, the customer. Our user-centric design philosophy is embedded in every interaction you have with us. From the layout of"
            "our showroom to the functionality of our online platform, we prioritize ease of use and clarity. Our goal is to make the car-buying process enjoyable and"
            "stress-free. We actively listen to customer feedback and adapt our services to meet evolving needs. At Winston's Automobiles, we believe that a"
            "user-centric approach ensures not only customer satisfaction but also builds lasting relationships based on trust and understanding."
        ),
    ]),

    html.Div(children=[
        html.H2("Join Us on the Journey"),
        html.Hr(),
        html.P(
            "Embark on this exciting journey with Winston's Automobiles and be a part of a community that values expertise, innovation, and user-centric design."
            "Join us as we redefine the pre-owned car buying experience, setting new standards in the industry and creating lasting relationships with our customers."
            "Winston's Automobiles is designed with you in mind. Thank you for being a part of our community. Let's redefine automobile industry together!"
        ),
    ]),
])
