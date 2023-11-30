from manim import *

#Other Ideas to Add
#add arc length? (total distance)
#put on github

class ProjectileMotion(Scene):
    def construct(self):
        
        # Set constants & inputs
        ACCELERATION = -9.8 #meters per second squared
        time = ValueTracker(0)
        initial_velocity = float(input("Initial Velocity (m/s):  ") or 30)
        initial_height = float(input("Initial Height (m):  ") or 13)
        angle_degrees = float(input("Launch Angle (degrees):  ") or 70)  # Launch angle in degrees
         
        # Convert angle to radians
        angle_radians = np.radians(angle_degrees)
        
        # Calculate initial horizontal and vertical velocities
        initial_horizontal_velocity = initial_velocity * np.cos(angle_radians)
        initial_vertical_velocity = initial_velocity * np.sin(angle_radians)

        # Calculate Time of Flight and arc dimensions
        time_of_flight = -(initial_velocity*np.sin(angle_radians)+np.sqrt((initial_velocity*np.sin(angle_radians))**2-2*ACCELERATION*initial_height))/ACCELERATION
        x_width = initial_horizontal_velocity*time_of_flight
        y_height = -(initial_velocity*np.sin(angle_radians))**2/(2*ACCELERATION) + initial_height

        # Functions to update ball's position
        def horizontal_motion():
            return lambda x : x.set_x(plane.c2p(initial_horizontal_velocity*time.get_value(),0)[0])

        def vertical_motion():
            return lambda y : y.set_y(plane.c2p(0,initial_height + initial_velocity*np.sin(angle_radians)*time.get_value() + 1/2*ACCELERATION*time.get_value()**2)[1])

        # Text Management
        title_text = Text("Projectile Motion Visualizer", font_size=46).to_edge(UP).shift(UP*0.25)
        
        acceleration_text = MathTex(r"\text{ACCELERATION: }", Acceleration, r"\:m/s^2")
        acceleration_text[1].set_color(PURPLE) #a

        init_vel_text = MathTex(r"\text{Initial Velocity: }", initial_velocity, "\:m/s")                        
        init_vel_text[1].set_color(BLUE) #init_vel

        init_height_text = MathTex(r"\text{Initial Height: }", initial_height, r"\:m")
        init_height_text[1].set_color(GREEN) #init_height

        init_angle_text = MathTex(r"\text{Launch Angle: }", angle_degrees, r"\:degrees")
        init_angle_text[1].set_color(RED) #init_angle

        time_value = always_redraw(lambda : Text(f'{time.get_value():.2f}', font_size=34))
        time_text = Tex(r"Time: ")

        x_vel_value = always_redraw(lambda : Text(f'{initial_horizontal_velocity:.2f}', font_size=34))
        x_vel_text = Tex(r"Horizontal Velocity: ")
        
        y_vel_value = always_redraw(lambda : Text(f'{initial_height + initial_velocity*time.get_value() + 1/2*ACCELERATION*time.get_value()**2:.2f}', font_size=34))
        y_vel_text = Tex(r"Vertical Velocity: ")
              
        #arc_len_value = always_redraw(lambda : Text(f'{initial_height:.2f}', font_size=34))
        #arc_len_text = Tex(r"Distance Traveled: ")

        text_group = VGroup(acceleration_text, init_height_text, init_vel_text, init_angle_text, time_text, x_vel_text, y_vel_text).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + LEFT).shift(DOWN*0.5)

        always_redraw(lambda : time_value.next_to(time_text, RIGHT))
        always_redraw(lambda : time_value.set_color(ORANGE))
        time_units = MathTex(r"\:s").next_to(time_value, RIGHT)
        
        always_redraw(lambda : x_vel_value.next_to(x_vel_text, RIGHT))
        always_redraw(lambda : x_vel_value.set_color(YELLOW))
        x_vel_units = MathTex(r"\:m/s").next_to(x_vel_value, RIGHT)
        
        always_redraw(lambda : y_vel_value.next_to(y_vel_text, RIGHT))
        always_redraw(lambda : y_vel_value.set_color(YELLOW))
        y_vel_units = MathTex(r"\:m/s").next_to(y_vel_value, RIGHT)

        # always_redraw(lambda : arc_len_value.next_to(arc_len_text, RIGHT))
        # always_redraw(lambda : arc_len_value.set_color(RED))
        # arc_len_units = MathTex(r"\:m").next_to(arc_len_value, RIGHT)
    
        kinematic_text_y = MathTex(r"{{v_{f(y)}}}={{x_{o(y)}}} + {{v_{i(y)}}}{{t}} + \frac{1}{2}{{a}}{{t^2}}").next_to(text_group, DOWN).shift(RIGHT*0.5)
        kinematic_text_y[0].set_color(YELLOW) # final_velocity
        kinematic_text_y[2].set_color(GREEN) #init_height
        kinematic_text_y[4].set_color(BLUE) #init_vel
        kinematic_text_y[6].set_color(ORANGE) #t
        kinematic_text_y[8].set_color(PURPLE) #a
        kinematic_text_y[9].set_color(ORANGE) #t

        # Setup NumberPlane
        plane = NumberPlane(
            x_range=[0,x_width,int(x_width/10)],
            y_range=[-1,y_height,int(y_height/10)],
            x_length=5,
            y_length=5,
            axis_config={'color': WHITE},
            x_axis_config={"include_tip": False},
            y_axis_config={"include_tip": False},
        ).add_coordinates()
        plane.to_edge(RIGHT)

        # Setup Ball
        ball = Circle(
            radius = 0.05,
            color = YELLOW,
            fill_opacity = 1
        )     
   
        ball.move_to([plane.c2p(0,0)[0],plane.c2p(0,initial_height)[1],0])
        ball.add_updater(horizontal_motion())
        ball.add_updater(vertical_motion())
        
        # Add Trace Line
        trace = TracedPath(ball.get_center, stroke_opacity=[0, 1])

        # Set Animations
        self.add(title_text, plane, ball, trace, text_group, kinematic_text_y, x_vel_value, x_vel_units, time_value, time_units, y_vel_value, y_vel_units)
        self.wait(2)
        self.play(time.animate(rate_func=linear, run_time=5).set_value(time_of_flight))
        self.wait(10)

