import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0#0:IDLE , 1:RUN , 2: JUMP, 3:ATTACK1, 4:ATTACK2, 5:HIT_Taken, 6:DEATH
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 200, 400))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cool = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True


    def load_images(self, sprite_sheet, animation_steps):
        #extract imahes from sprites sheets
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale,  self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list




    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0


        #get key presses
        key = pygame.key.get_pressed()

        # can only perform actions if currently ont attacking
        #Player 1
        if self.player == 1:
            if self.attacking == False and self.alive == True and round_over ==  False:
                #movement()
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                elif key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump movements
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -50
                    self.jump = True


                #attacking
                if key[pygame.K_q] or key[pygame.K_e]:
                    self.attack(surface, target)
                    if key[pygame.K_q]:
                        self.attack_type = 1
                        self.attacking = True
                    if key[pygame.K_e]:
                        self.attack_type = 2
                        self.attacking = True





            #applying Gravity
            self.vel_y += GRAVITY
            dy+=self.vel_y

            # ensure payer is on Screen
            if self.rect.left + dx < 0:
                dx = +self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 50:
                self.vel_y = 0
                self.jump = False
                dy = screen_height - 50 - self.rect.bottom






            #Ensure  playes face each other
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # apply cooldown
            while self.attack_cool > 0:
                self.attack_cool -= 1

            #update player
            self.rect.x +=dx
            self.rect.y +=dy


        #player 2
        if self.player == 2:
            if self.attacking == False  and self.alive == True and round_over ==  False:
                # movement()
                if key[pygame.K_KP6]:
                    dx = SPEED
                    self.running = True
                elif key[pygame.K_KP4]:
                    dx = -SPEED
                    self.running = True
                # jump movements
                if key[pygame.K_KP8] and self.jump == False:
                    self.vel_y = -50
                    self.jump = True

                # attacking
                if key[pygame.K_KP7] or key[pygame.K_KP9]:
                    self.attack(surface, target)
                    if key[pygame.K_KP7]:
                        self.attack_type = 1
                        self.attacking = True
                    if key[pygame.K_KP9]:
                        self.attack_type = 2
                        self.attacking = True

            # applying Gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            # ensure payer is on Screen
            if self.rect.left + dx < 0:
                dx = +self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 50:
                self.vel_y = 0
                self.jump = False
                dy = screen_height - 50 - self.rect.bottom

            # Ensure  playes face each other
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # apply cooldown
            while self.attack_cool > 0:
                self.attack_cool -= 1

            # update player
            self.rect.x += dx
            self.rect.y += dy



    #handle animation updates
    def update(self):
        animation_cooldown = 100  # 0.5seconds
        #check what action user is performing
        if self.health <= 0:
            self.alive = False
            self.update_action(6)#death
        elif self.hit == True:
            self.update_action(5)#Hit takken
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)#ATTACK_TYPE_1
                animation_cooldown = 25
            elif self.attack_type == 2:
                self.update_action(4)#ATTACK_TYPE_2
                animation_cooldown = 25
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action (1)#RUNNING
        else:
            self.update_action(0)#IDLE
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time is passed
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >=len(self.animation_list[self.action]):
            #check if the player is dead
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
        #check if attacking was executed
        if self.action == 3 or self.action == 4:
            self.attacking = False
            self.attack_cool = 10
        #check if the hit has been taken
        if self.action == 5:
            self.hit = False
            #if the payer who is middle of the attack then the attack is stopped
            self.attacking = False
            self.attack_cool = 10





    def attack(self, surface, target):
        self.attacking = True
        if self.attack_cool == 0 and self.attacking == True:
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 5
                target.hit = True
            #pygame.draw.rect(surface, (0, 255,0), attacking_rect)

    #helper function
    def update_action(self, new_action):
        #check if the new action is different to the previcous one
        if new_action != self.action:
            self.action = new_action
            #update the animation setting
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def draw(self, surface):
        img = pygame.transform .flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[0] * self.image_scale)))


