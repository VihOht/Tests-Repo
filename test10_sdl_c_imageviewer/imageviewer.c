#include <stdio.h>
#include <string.h>
#include <SDL2/SDL.h>

int main() {
	
	// Initiating SDL, app window and app surface
	SDL_Init(SDL_INIT_VIDEO);
	SDL_Window *appw;
	SDL_Surface *apps;

	// Loading file
	FILE *file = stdin;

	// Reading from stdin the format, the size
	const int BUFFER_SIZE=1000;
	char buffer[BUFFER_SIZE];

	// Getting image ppm format
	fgets(buffer, BUFFER_SIZE, file);
	printf("Image ppm format:  %s", &buffer);

	// Geting image commentary
	fgets(buffer, BUFFER_SIZE, file);
	printf("%s", &buffer);

	// Getting image size
	int width;
	int height;
	fgets(buffer, BUFFER_SIZE, file);
	sscanf(buffer, "%d %d", &width, &height);
	printf("Image size: width=%d, heigth=%d\n", width, height);;

	// Getting image maximum color value
	int maxColor;
	fgets(buffer, BUFFER_SIZE, file);
	sscanf(buffer, "%d", &maxColor);
	printf("MaxColor: %d", maxColor);


	// Defining some constants our windo will have
	const char *title = "ImageViewer";

	//  Creating a window 
	appw = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, 0);

	apps = SDL_GetWindowSurface(appw);
	
	// Drawing a vertical Line
	int y;
	int middleY = height / 2;
	SDL_Rect pixel = (SDL_Rect){0, 0, 1, 1};
	Uint32 color = 0; 
	for (int y= 0; y<width; y++){
		for (int x=0; x<height; x++){
			Uint8 r, g, b;
			r = (char) getchar();
			g = (char) getchar();
			b = (char) getchar();

			r = (r *  255) / maxColor;
			g = (g * 255) / maxColor;
			b = (b * 255) / maxColor;

			color = SDL_MapRGB(apps->format, r, g, b);
			pixel.x=x;
			pixel.y=y;
			SDL_FillRect(apps, &pixel, color);
		}
	}
	SDL_UpdateWindowSurface(appw);

	 bool running = true;
	 while(running) {
		SDL_Event event;
		while(SDL_PollEvent(&event)){
			if(event.type == SDL_QUIT){
				running = false;
			}
		}
	}



	 SDL_DestroyWindow(appw);
	 SDL_Quit();
	 return 0;
}
