//
//  OnboardingTestimonial.swift
//  OnboardingCinematicView
//
//  Created by Adam Lyttle on 8/8/2025.
//

import SwiftUI
import AVKit

struct OnboardingCinematicView: View {
    
    @Binding var isPresented: Bool

    @State private var step: Int = 0
    @State private var animatedStep: Int = 0
    @State private var onboardingOpacity: Double = 1
    
    
    var body: some View {
        
        ZStack {
            
            OnboardingHeaderView()
            
            VStack(spacing: 30) {
                //OnboardingVideoView()
                
                OnboardingProgressView(step: $animatedStep)
                
                VStack {
                    if step == 0 {
                        //first screen
                        
                        VStack {
                            VStack (spacing: 20) {
                                Text("Welcome to Insect Identifier")
                                    .font(.largeTitle.bold())
                                    .multilineTextAlignment(.center)
                                Text("The most accurate and efficient way to identify insects & spiders")
                                    .multilineTextAlignment(.center)
                                    .opacity(0.8)
                            }
                            .padding(.horizontal)
                        }
                        .padding(.horizontal)
                        
                        Spacer()
                        
                        OnboardingTestimonialView()
                        
                        Spacer()
                        
                    }
                    else if step == 1 {
                        
                        VStack {
                            VStack (spacing: 20) {
                                Text("Snap a Photo to Identify Insects & Spiders")
                                    .font(.largeTitle.bold())
                                    .multilineTextAlignment(.center)
                                Text("Quickly and accurately discover insect and spider species with a single photo. Simply snap and identify!")
                                    .multilineTextAlignment(.center)
                                    .opacity(0.8)
                            }
                            .padding(.horizontal)
                        }
                        .padding(.horizontal)
                        
                        Spacer()
                        
                        CustomAnimationFishPhotoView()
                        
                        Spacer()
                        
                    }
                    else if step == 2 {
                        
                        VStack {
                            VStack (spacing: 20) {
                                Text("Powered by AI")
                                    .font(.largeTitle.bold())
                                    .multilineTextAlignment(.center)
                                Text("Experience the power of AI for instant and accurate insect identification, tailored to your current location")
                                    .multilineTextAlignment(.center)
                                    .opacity(0.8)
                            }
                            .padding(.horizontal)
                        }
                        .padding(.horizontal)
                        
                        Spacer()
                        
                        CustomAnimationDigitalSharkView() //Text("[animation here]")
                        
                        Spacer()
                        
                    }
                    
                    VStack (spacing: 25) {
                        
                        Button(action: {
                            nextStep()
                        }) {
                            HStack {
                                Spacer()
                                Text("Continue")
                                    .font(.title3.bold())
                                Spacer()
                            }
                            .padding()
                        }
                        .background {
                            RoundedRectangle(cornerRadius: 12)
                                .foregroundColor(Color.red)
                        }
                        .accentColor(.white)
                        
                        HStack {
                            if step == 0 {
                                Image(systemName: "magnifyingglass")
                                    .foregroundColor(Color.red)
                                Text("Trusted by 2,536+ Entomology Enthusiasts")
                                    .bold()
                            }
                            else if step == 1 {
                                Image(systemName: "photo.fill")
                                    .foregroundColor(Color.red)
                                Text("Over 7,634+ Insects Identified")
                                    .bold()
                            }
                            else if step == 2 {
                                Image(systemName: "ladybug.fill")
                                    .foregroundColor(Color.red)
                                Text("Trained on 1,427,523+ Insect Species")
                                    .bold()
                            }
                        }
                        .font(.caption)
                    }
                    .padding()
                }
                .opacity(onboardingOpacity)
            }
            
        }
        .preferredColorScheme(.dark)

    }
    
    func nextStep() {
        if step == 2 {
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
                isPresented = false
            }
        }
        else {
            withAnimation(.easeInOut(duration: 0.5)) {
                onboardingOpacity = 0
            }
            withAnimation(.easeInOut(duration: 1.0)) {
                animatedStep = step + 1
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                step += 1
                withAnimation(.easeInOut(duration: 0.5)) {
                    onboardingOpacity = 1
                }
            }
        }
    }
    
    
    
}


struct OnboardingTestimonial {
    var id: Int
    var title: String
    var description: String
}


struct OnboardingProgressView: View {
    @Binding var step: Int
    var body: some View {
        HStack {
            ZStack {
                Circle().foregroundColor(step >= 0 ? Color.red : Color.white.opacity(0.3))
                Image(systemName: "ladybug.fill")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(maxWidth: 20, maxHeight: 20, alignment: .center)
                    .clipped()
            }
            .foregroundColor(.white)
            .scaleEffect(step >= 0 ? 1.2 : 0.8)
            .frame(width: 30, height: 30)
            
            Spacer()
                .background {
                    Rectangle()
                        .frame(width: .infinity, height: 2)
                        .foregroundColor(step > 0 ? Color.red : Color.white.opacity(0.1))
                        .padding(.horizontal)
                }
            
            ZStack {
                Circle().foregroundColor(step >= 1 ? Color.red : Color.white.opacity(0.3))
                //Circle().foregroundColor(.black)
                Image(systemName: step >= 1 ? "camera.fill" : "camera")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(maxWidth: 20, maxHeight: 20, alignment: .center)
                    .clipped()
                    .opacity(step >= 1 ? 1.0 : 0.5)
            }
            .foregroundColor(.white)
            .scaleEffect(step >= 1 ? 1.2 : 0.8)
            .frame(width: 30, height: 30)
            
            Spacer()
                .background {
                    Rectangle()
                        .frame(width: .infinity, height: 2)
                        .foregroundColor(step > 1 ? Color.red : Color.white.opacity(0.1))
                        .padding(.horizontal)
                }
            
            
            ZStack {
                Circle().foregroundColor(step >= 2 ? Color.red : Color.white.opacity(0.3))
                //Circle().foregroundColor(.black)
                Image(systemName: step >= 2 ? "sparkles" : "sparkles")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(maxWidth: 20, maxHeight: 20, alignment: .center)
                    .clipped()
                    .opacity(step >= 2 ? 1.0 : 0.5)
            }
            .foregroundColor(.white)
            .scaleEffect(step >= 2 ? 1.2 : 0.8)
            .frame(width: 30, height: 30)
            
        }
        .padding(.vertical)
        .padding(.horizontal, 50)
    }
}

struct OnboardingTestimonialView: View {
    
    @State private var hasSeenTestimonial = false
    @State private var testimonialOpacity: CGFloat = 0.0
    @State private var testimonials: [OnboardingTestimonial] = [
        OnboardingTestimonial(id: 1, title: "Such a good app", description: ""),
        //OnboardingTestimonial(id: 2, title: "So Good", description: "I can just scan the fish I catch and it will give me the name facts and so much more"),
    ]
    @State private var hasInit: Bool = false
    
    var body: some View {
        VStack {
            
            if let testimonial = testimonials.first {
                VStack {
                    VStack (spacing: 30) {
                        HStack (alignment: .bottom) {
                            
                            Spacer()
                            
                            Image("award-leaves")
                                .resizable()
                                .aspectRatio(contentMode: .fit)
                                .frame(width: 45, alignment: .center)
                                .clipped()
                                .scaleEffect(1.2)
                        
                            
                            VStack {
                                Image("avatar-\(testimonial.id)")
                                    .resizable()
                                    .aspectRatio(contentMode: .fit)
                                    .frame(width: 90, height: 90)
                                    .clipped()
                                    .mask {
                                        Circle()
                                    }
                                    .padding(.horizontal)
                                
                                VStack (spacing: 9) {
                                    
                                    
                                    Text(testimonial.title)
                                        .lineLimit(1)
                                        .truncationMode(.tail)
                                        .layoutPriority(100)
                                        .font(.title2.italic())
                                    
                                    HStack (spacing: 3) {
                                        Image(systemName: "star.fill")
                                            .foregroundColor(.yellow)
                                        Image(systemName: "star.fill")
                                            .foregroundColor(.yellow)
                                        Image(systemName: "star.fill")
                                            .foregroundColor(.yellow)
                                        Image(systemName: "star.fill")
                                            .foregroundColor(.yellow)
                                        Image(systemName: "star.fill")
                                            .foregroundColor(.yellow)
                                    }
                                    
                                    
                                }
                                .padding()
                                
                            }
                            
                            
                            Image("award-leaves")
                                .resizable()
                                .aspectRatio(contentMode: .fit)
                                .frame(width: 45, alignment: .center)
                                .clipped()
                                .scaleEffect(x: -1, y: 1, anchor: .center) // Mirroring the image horizontally
                                .scaleEffect(1.2)
                            
                            Spacer()
                            
                        }
                        
                        if !testimonial.description.isEmpty {
                            Text("\"\(testimonial.description)\"")
                                .multilineTextAlignment(.center)
                                .italic()
                        }
                        
                        
                    }
                    .padding()
                    
                    
                }
                .background {
                    ZStack {
                        RoundedRectangle(cornerRadius: 10)
                            .foregroundColor(Color.black.opacity(0.03))
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(Color.black.opacity(0.1), lineWidth: 1)
                    }
                }
                .opacity(testimonialOpacity)
                .scaleEffect(testimonialOpacity == 1 ? 1 : 2)
                .blur(radius: testimonialOpacity == 1 ? 0 : 20)
                .rotationEffect(.degrees(testimonialOpacity == 1 ? 0 : 30))
                
                .onAppear {
                    if !hasSeenTestimonial {
                        hasSeenTestimonial = true
                        nextTestimonial()
                    }
                }
                .frame(minHeight: 100)
            }
            
        }
        .padding(.horizontal)
        .onAppear {
            testimonials.shuffle()
        }
    }
    
    func nextTestimonial() {
        
        
        if let firstTestimonial = testimonials.first {
            testimonials.append(firstTestimonial)
            testimonials.remove(at: 0)
        }
        
        
        withAnimation {
            testimonialOpacity = 1.0
        }
        
        if testimonials.count > 1 {
            DispatchQueue.main.asyncAfter(deadline: .now() + 3.4) {
                withAnimation {
                    testimonialOpacity = 0.0
                }
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
                    nextTestimonial()
                }
            }
        }
        
    }
    
}


struct OnboardingHeaderView: View {
    var body: some View {
        VStack {
            Image("hero-header")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .clipped()
            Spacer()
            Image("hero-footer")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .clipped()
                .opacity(0.5)
        }
        .ignoresSafeArea()
    }
}

struct CustomAnimationDigitalSharkView: View {
    
    @State private var firstRowPosition: CGFloat = 0
    @State private var secondRowPosition: CGFloat = 0
    @State private var thirdRowPosition: CGFloat = 0
    @State private var allOpacity: CGFloat = 0
    
    var body: some View {
        ZStack {
            
            ScrollView(.horizontal) {
                VStack (alignment: .leading, spacing: 5) {
                    Text("0101010101110000011001110111001001100001011001000110010100100000011101000110111100100000011101000110100001100101001000000111000001110010011001010110110101101001011101010110110100100000011101100110010101110010011100110110100101101111011011100010000001100001011011100110010000100000011101000110")
                        .offset(x: -firstRowPosition)
                    Text("0101010101110000011001110111001001100001011001000110010100100000011101000110111100100000011101000110100001100101001000000111000001110010011001010110110101101001011101010110110100100000011101100110010101110010")
                        .offset(x: -secondRowPosition)
                    Text("0010111010101101101001000000111011001100101011100100111001101101001011011110110111000100000011000010110111001100100001000000111010001100001011010110110010100100000011000010111000001101000011011110111010001101111001000000110111101100110001000000111100101101111011101010111001000100000011001100110100")
                        .offset(x: -thirdRowPosition)
                }
                .font(.system(size: 50).bold())
                .foregroundColor(Color.red)
            }
            .opacity(allOpacity)
            
            Image("onboarding-shark")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .clipped()
        }
        .onAppear {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                doAnimation()
            }
        }
    }
    
    func doAnimation() {
        
        firstRowPosition = 0
        secondRowPosition = 0
        thirdRowPosition = 0
        
    
        withAnimation(.easeInOut(duration: 0.4)) {
            allOpacity = 1
        }
    
        withAnimation(.linear(duration: 10.6)) {
            firstRowPosition = 400
            secondRowPosition = 1000
            thirdRowPosition = 800
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 10.6 - 1.0) {
            withAnimation(.easeInOut(duration: 0.4)) {
                allOpacity = 0
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
                doAnimation()
            }
        }
        
    }
}

struct CustomAnimationFishPhotoView: View {
    
    @State private var handOpacity: CGFloat = 0
    @State private var flashOpacity: CGFloat = 0
    @State private var identifiedOpacity: CGFloat = 0
    @State private var allOpacity: CGFloat = 0
    
    var body: some View {
        ZStack {
            Image("onboarding-fish-wireframe")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .clipped()
                .padding()
                //.blur(radius: handOpacity == 0 ? 0 : 20)
                .opacity(handOpacity == 0 ? 1 : 0.4 )
                .scaleEffect(handOpacity == 0 ? 1.0 : 1.1)
                .blur(radius: handOpacity == 0 ? 0 : 4)
        
            ZStack {
                if identifiedOpacity == 0 {
                    Image("onboarding-hand-animation-1")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .clipped()
                        .padding()
                    //.opacity(flashOpacity==1 ? 0 : 1)
                    Image("onboarding-hand-animation-2")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .clipped()
                        .padding()
                        .opacity(identifiedOpacity == 0 ? flashOpacity : 0)
                }
                Image("onboarding-hand-animation-3")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .clipped()
                    .padding()
                    .opacity(identifiedOpacity)
            }
            .scaleEffect(handOpacity == 0 ? 1.5 : 1.0)
            .opacity(handOpacity)
        }
        .opacity(allOpacity)
        .onAppear {
            //fix glitch error:
            handOpacity = 1
            flashOpacity = 1
            identifiedOpacity = 0
            allOpacity = 0.001
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                doAnimation()
            }
        }
    }
    
    func doAnimation() {
        
        handOpacity = 0
        flashOpacity = 0
        identifiedOpacity = 0
        allOpacity = 0
        
        withAnimation(.easeInOut(duration: 0.4)) {
            allOpacity = 1
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
            
            //hand moves in
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                withAnimation(.easeInOut(duration: 1.7)) {
                    handOpacity = 1
                }
                //phone animation chain, starting with flash going off
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.5 ) {
                    withAnimation(.easeInOut(duration: 0.2)) {
                        flashOpacity = 1
                    }
                    //fish identification animation:
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                        withAnimation(.easeInOut(duration: 0.2)) {
                            identifiedOpacity = 1
                        }
                        //fade to black
                        DispatchQueue.main.asyncAfter(deadline: .now() + 2.3) {
                            withAnimation(.easeInOut(duration: 0.4)) {
                                allOpacity = 0
                            }
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
                                doAnimation()
                            }
                        }
                    }
                }
            }
        }
        
    }
}
