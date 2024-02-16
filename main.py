import sys
from script_generator import generate_script

def main():  
    script = generate_script()

    if not script:
        print("Error generating script")
        sys.exit()

    video_title = script['title']
    video_script = script['content']
    print(video_script)


if __name__ == '__main__':
    main()