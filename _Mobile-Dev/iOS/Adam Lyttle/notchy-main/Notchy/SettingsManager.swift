import Foundation

@Observable
class SettingsManager {
    static let shared = SettingsManager()

    var showNotch: Bool {
        didSet { UserDefaults.standard.set(showNotch, forKey: "replaceNotch") }
    }

    var soundsEnabled: Bool {
        didSet { UserDefaults.standard.set(soundsEnabled, forKey: "soundsEnabled") }
    }

    var xcodeIntegrationEnabled: Bool {
        didSet { UserDefaults.standard.set(xcodeIntegrationEnabled, forKey: "xcodeIntegrationEnabled") }
    }

    var claudeIntegrationEnabled: Bool {
        didSet { UserDefaults.standard.set(claudeIntegrationEnabled, forKey: "claudeIntegrationEnabled") }
    }

    init() {
        let defaults = UserDefaults.standard
        if defaults.object(forKey: "replaceNotch") == nil { defaults.set(true, forKey: "replaceNotch") }
        if defaults.object(forKey: "soundsEnabled") == nil { defaults.set(true, forKey: "soundsEnabled") }
        if defaults.object(forKey: "xcodeIntegrationEnabled") == nil { defaults.set(true, forKey: "xcodeIntegrationEnabled") }
        if defaults.object(forKey: "claudeIntegrationEnabled") == nil { defaults.set(true, forKey: "claudeIntegrationEnabled") }

        showNotch = defaults.bool(forKey: "replaceNotch")
        soundsEnabled = defaults.bool(forKey: "soundsEnabled")
        xcodeIntegrationEnabled = defaults.bool(forKey: "xcodeIntegrationEnabled")
        claudeIntegrationEnabled = defaults.bool(forKey: "claudeIntegrationEnabled")
    }
}
