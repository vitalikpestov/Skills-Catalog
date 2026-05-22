//
//  ContentView.swift
//  OnboardingCinematicView
//
//  Created by Adam Lyttle on 8/8/2025.
//

import SwiftUI

@main
struct OnboardingCinematicViewApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @State private var isPresented = true
    var body: some View {
        Text("Hello, world!")
            .fullScreenCover(isPresented: $isPresented) {
                OnboardingCinematicView(
                    isPresented: $isPresented
                )
            }
    }
    
}

#Preview {
    ContentView()
}
