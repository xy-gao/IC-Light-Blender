from  gradio_demo import process_relight
import cv2


if __name__ == "__main__":
    input_img = cv2.cvtColor(cv2.imread('imgs/untitled.png', cv2.IMREAD_UNCHANGED), cv2.COLOR_RGBA2BGRA)
    print(input_img)
    input_fg = input_img[:,:,:-1]
    input_a = input_img[:,:,-1]
    prompt = "sunset"
    image_width = int(input_fg.shape[1] /2)
    image_height = int(input_fg.shape[0] /2)
    # image_width = 512
    # image_height = 640
    num_samples = 1
    seed = 12345
    steps = 25
    a_prompt = 'best quality'
    n_prompt = 'lowres, bad anatomy, bad hands, cropped, worst quality'
    cfg = 2
    highres_scale = 1.5
    highres_denoise = 0.5
    lowres_denoise = 0.9
    bg_source = "Top Light"

    cv2.imwrite('output1.png', input_img)
    output_bg, result_gallery = process_relight(input_fg, input_a, prompt, image_width, image_height, num_samples, seed, steps, a_prompt, n_prompt, cfg, highres_scale, highres_denoise, lowres_denoise, bg_source)

    cv2.imwrite('output2.png', cv2.cvtColor(result_gallery[0], cv2.COLOR_RGB2BGR))
